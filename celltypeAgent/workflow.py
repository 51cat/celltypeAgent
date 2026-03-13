import os
import glob
from concurrent.futures import ThreadPoolExecutor

from celltypeAgent import load_json, write_json
from celltypeAgent.tools.utils import add_log
from celltypeAgent.tools.logger import (
    log_info, log_warning, log_success, 
    display_annotation_table, display_section_header
)
from celltypeAgent.state.state import SingleCluster, MetaData, ClusterInfo

from celltypeAgent.llm.n1n import N1N_LLM

from celltypeAgent.nodes.paramcollector_node import ParamCollectorNode 
from celltypeAgent.nodes.anno_cluster_node import CelltypeAnnoNode
from celltypeAgent.nodes.audit_ann_node import CelltypeAnnAuditNode
from celltypeAgent.nodes.consensus_node import CelltypeConsensusNode
from celltypeAgent.nodes.report_node import CelltypeReportNode
from celltypeAgent import get_llm_config_value



PARM_COLLECT_MODEL = 'gpt-5.4'
REPORT_MODEL       = 'claude-sonnet-4-6'
ANNOTATION_MODEL   =  ['gpt-5.4', 'claude-sonnet-4-6','qwen3.5-397b-a17b', 'grok-4.2', 'glm-5', 'deepseek-v3.2']
AUDIT_MODEL        = 'claude-sonnet-4-6'
CONSENSUS_MODEL     = 'claude-sonnet-4-6'
MAX_REFLECT_TIMES   = 5
RELIABILITY_THRESHOLD = 70

class CelltypeWorkflow:
    def __init__(self, marker_table, outdir, provider= 'n1n'):
        self.llm_config_dict = get_llm_config_value(provider)
        self.marker_table = marker_table
        self.outdir = outdir
        self.metadata_state = MetaData()

        self._initialize_metadata_state()
        self._initialize_client()
        self._initialize_nodes()

    @add_log
    def _initialize_metadata_state(self):
        self.metadata_state.update_matadata('marker_table', self.marker_table)
        self.metadata_state.update_matadata('api', self.llm_config_dict['api'])
        self.metadata_state.update_matadata('base_url', self.llm_config_dict['base_url'])
        self.metadata_state.update_matadata('parm_collect_model', PARM_COLLECT_MODEL)
        self.metadata_state.update_matadata('annotation_model', ANNOTATION_MODEL)
        self.metadata_state.update_matadata('audit_model', AUDIT_MODEL)
        self.metadata_state.update_matadata('consensus_model', CONSENSUS_MODEL)
        self.metadata_state.update_matadata('report_model', REPORT_MODEL)

        self.metadata_state.update_matadata('outdir', f"{self.outdir}/")

        
    @add_log
    def _initialize_client(self):

        self.parm_collect_client = N1N_LLM(
            api_key = self.metadata_state.get_metadata_val('api'),
            model_name = self.metadata_state.get_metadata_val('parm_collect_model'),
            base_url = self.metadata_state.get_metadata_val('base_url')
        )

        self.annotation_clients = [
             N1N_LLM(api_key = self.metadata_state.get_metadata_val('api'), 
                model_name = model_name, base_url = self.metadata_state.get_metadata_val('base_url')) 
             for model_name in self.metadata_state.get_metadata_val('annotation_model')
        ]

        self.audit_client = N1N_LLM(
            api_key = self.metadata_state.get_metadata_val('api'),
            model_name = self.metadata_state.get_metadata_val('audit_model'),
            base_url = self.metadata_state.get_metadata_val('base_url'))
        
        self.consensus_client = N1N_LLM(api_key = self.metadata_state.get_metadata_val('api'),
            model_name = self.metadata_state.get_metadata_val('consensus_model'),
            base_url = self.metadata_state.get_metadata_val('base_url'))
        
        self.report_client = N1N_LLM(api_key = self.metadata_state.get_metadata_val('api'),
            model_name = self.metadata_state.get_metadata_val('report_model'),
            base_url = self.metadata_state.get_metadata_val('base_url'))

    @add_log
    def _initialize_nodes(self):
        self.pnode = ParamCollectorNode(self.parm_collect_client, self.metadata_state)
    
    @add_log
    def _ann_single_cluster(self, cluster_id = 0):
        
        display_section_header(f"Cluster {cluster_id} 注释流程", "🔬")
        
        cluster_state = SingleCluster(cluster_id=cluster_id, 
                                      cluster_genes=self.cluster_gene_state.get_cluster_genes(cluster_id))
        
        annotation_results = []
        
        for llm in self.annotation_clients:
            model_name = llm.get_model_info()['model']
            log_info(f"开始 [bold]{model_name}[/bold] 模型注释 cluster 「{cluster_id}」...", highlight=True)
            
            cnode = CelltypeAnnoNode(self.metadata_state, cluster_state)
            cnode.set_LLM(llm)
            cnode.prep()
            res_ann = cnode.run()
            cluster_state.update_ann_results(model_name, res_ann)

            audit_node = CelltypeAnnAuditNode(self.audit_client, self.metadata_state, cluster_state)
            audit_node.prep(model_name)
            res_audio = audit_node.run()
            cluster_state.update_audit_results(model_name, res_audio)

            score = res_audio['reliability_score']
            reflect_times = 0

            while score < RELIABILITY_THRESHOLD:
                reflect_times += 1

                log_warning(f"模型 {model_name} 不可靠，第 {reflect_times} 次反思修正，cluster 「{cluster_id}」...")
                
                res_ann = cnode.reflect_ann(res_ann)
                cluster_state.update_ann_results(model_name, res_ann)

                res_audio = audit_node.reflect_audit(res_audio)
                cluster_state.update_audit_results(model_name, res_audio)

                score = res_audio['reliability_score']

                if reflect_times >= MAX_REFLECT_TIMES:
                    log_warning(f"模型 {model_name} 经过 {MAX_REFLECT_TIMES} 次反思仍不可靠，cluster 「{cluster_id}」标记为 Unreliable，停止反思")
                    cell_type = cluster_state.get_celltype(model_name)
                    cell_subtype = cluster_state.get_cell_subtype(model_name)

                    cluster_state.update_cell_subtype(model_name, f'(Unreliable)_{cell_type}')
                    cluster_state.update_cell_subtype(model_name, f'(Unreliable)_{cell_subtype}')
                    break

            log_success(f"模型 {model_name} 完成 cluster 「{cluster_id}」，可靠性评分: {score}")
            
            annotation_results.append({
                "model": model_name,
                "cell_type": cluster_state.get_celltype(model_name),
                "cell_subtype": cluster_state.get_cell_subtype(model_name),
                "score": score
            })
        
        display_annotation_table(annotation_results, f"Cluster {cluster_id} 注释结果")
        
        log_info(f"开始共识检验...", highlight=True)
        
        connode = CelltypeConsensusNode(self.consensus_client, self.metadata_state, cluster_state)
        connode.prep()
        res_con = connode.run()
        cluster_state.updata_consensus_results(res_con)

        log_success(f"共识检验完成")

        log_info(f"生成报告...", highlight=True)
        
        rnode = CelltypeReportNode(self.report_client, cluster_state)
        rnode.prep()
        res_report = rnode.run()

        outdir = self.metadata_state.get_metadata_val('outdir')
        log_outdir = f"{outdir}/log/{cluster_id}/"
        report_dir = f"{outdir}/report/"

        if not os.path.exists(log_outdir):
            os.makedirs(log_outdir, exist_ok=True)
        
        if not os.path.exists(report_dir):
            os.makedirs(report_dir, exist_ok=True)
        
        write_json(cluster_state.ann_to_dict(), f"{log_outdir}/ann_results.json")
        write_json(cluster_state.audit_to_dict(), f"{log_outdir}/audit_results.json")
        write_json(cluster_state.consensus_to_dict(), f"{log_outdir}/consensus_results.json")
        write_json(MetaData.to_dict(self.metadata_state), f"{log_outdir}/metadata.json")

        with open(f"{report_dir}/report_{cluster_id}.md", 'w', encoding='utf-8') as f:
            f.write(res_report)
        
        log_success(f"Cluster {cluster_id} 处理完成，结果已保存")
        
                
    @add_log
    def collect_parms(self):
        self.pnode.prep()
        is_complate, results = self.pnode.run()

        if not is_complate:
            raise Exception("参数收集失败，无法继续执行注释流程")
        
        # update metadata state
        for k, v in results['metadata'].items():
            self.metadata_state.update_matadata(k, v)

        self.cluster_gene_state = ClusterInfo(results['cluster'])
    
    def multi_cluster_annotation(self):
        cluster_ids = self.cluster_gene_state.get_all_cluster()

        for cluster_id in cluster_ids:
            self._ann_single_cluster(cluster_id)
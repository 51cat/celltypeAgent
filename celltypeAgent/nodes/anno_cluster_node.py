from celltypeAgent.prompt.prompt import INIT_CELLTYPE
from celltypeAgent.llm.n1n import N1N_LLM
from celltypeAgent.llm.message import Message
from celltypeAgent.tools.utils import extract_and_validate_json

class CelltypeAnnoNode:
    def __init__(self, LLM, cluster, genes, spec, tissue) -> None:
        self.llm = LLM
        self.cluster = cluster
        self.gene = ','.join(genes)
        self.spec = spec
        self.tissue = tissue
    
    def prep(self):
        self.system_prompt = INIT_CELLTYPE.format(
        species=self.spec,
        tissue=self.tissue,
        cluster_id=self.cluster,
        gene_list=self.gene
        )

    def run(self):
        message_input = Message(system_prompt=self.system_prompt)
        message_input.add_user_message('请开始进行注释任务！务必严格遵守我的要求！')
        response = self.llm.invoke_stream(message_input)
        res = extract_and_validate_json(response)
        print(res)
        


def main():

    llm_grok = N1N_LLM(
        api_key = 'sk-VW019xQdJlI0EJKpESIj8UcUYWTMyBop78hsJQ2W5P8ppe3D',
        model_name = 'grok-3',
        base_url = "https://api.n1n.ai/v1"
    )
    llm_gpt = N1N_LLM(
        api_key = 'sk-VW019xQdJlI0EJKpESIj8UcUYWTMyBop78hsJQ2W5P8ppe3D',
        model_name = 'deepseek-v3.2',
        base_url = "https://api.n1n.ai/v1"
    )
    cluster_name = "Cluster_7"
    markers = ["PTPRC", "CD3D", "CD4", "IL7R", "CCR7"]
    context = "Peripheral Blood Mononuclear Cells (PBMC)"

    pcnode = CelltypeAnnoNode(llm_grok,cluster_name,markers,'human',context)
    pcnode.prep()
    a = pcnode.run()

    pcnode = CelltypeAnnoNode(llm_gpt,cluster_name,markers,'human',context)
    pcnode.prep()
    a = pcnode.run()
    

    

if __name__ == '__main__':
    main()


        
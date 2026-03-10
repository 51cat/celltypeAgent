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
    
    def set_language(self, language):
        self.language = language

    def prep(self):
        self.system_prompt = INIT_CELLTYPE.format(
        species=self.spec,
        tissue=self.tissue,
        cluster_id=self.cluster,
        gene_list=self.gene,language= self.language
        )

    def run(self):
        message_input = Message(system_prompt=self.system_prompt)
        message_input.add_user_message('请开始进行注释任务！务必严格遵守我的要求！')
        response = self.llm.invoke(message_input)
        res = extract_and_validate_json(response)
        return res

        
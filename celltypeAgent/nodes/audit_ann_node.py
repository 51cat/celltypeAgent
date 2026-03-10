from celltypeAgent.prompt.prompt import AUDIT_PROMPT
from celltypeAgent.llm.n1n import N1N_LLM
from celltypeAgent.llm.message import Message
from celltypeAgent.tools.utils import extract_and_validate_json

import json

class CelltypeAnnAuditNode:
    def __init__(self, LLM, ann_dict) -> None:
        self.llm = LLM
        self.ann_dict = ann_dict

    def prep(self):
        
        self.system_prompt = AUDIT_PROMPT.format(
            species=self.ann_dict['spec'],
            tissue=self.ann_dict['tissue'],
            model_name=self.ann_dict['model'],
            genes=self.ann_dict['genes'],
            language=self.ann_dict['language'],
            cell_type=self.ann_dict['cell_type'],
            cell_subtype=self.ann_dict['cell_subtype'],
            reasoning=json.dumps(self.ann_dict['reasoning'], ensure_ascii=False)
        )
        
    def run(self):
        message_input = Message(system_prompt=self.system_prompt)
        message_input.add_user_message('请开始进行注释结果评价任务！务必严格遵守我的要求！')
        response = self.llm.invoke(message_input)
        res = extract_and_validate_json(response)
        return res
from celltypeAgent.llm.n1n import N1N_LLM

from celltypeAgent.nodes.paramcollector_node import ParamCollectorNode 
from celltypeAgent.nodes.anno_cluster_node import CelltypeAnnoNode
 


# test

llm = N1N_LLM(
        api_key = 'sk-VW019xQdJlI0EJKpESIj8UcUYWTMyBop78hsJQ2W5P8ppe3D',
        model_name = 'deepseek-v3.2',
        base_url = "https://api.n1n.ai/v1"
)

llm_gpt = N1N_LLM(
        api_key = 'sk-VW019xQdJlI0EJKpESIj8UcUYWTMyBop78hsJQ2W5P8ppe3D',
        model_name = 'gpt-5.4',
        base_url = "https://api.n1n.ai/v1"
    )

pcnode = ParamCollectorNode(llm, '/home/zhliu/test/p11/celltypeAgent/deg_all.csv')
pcnode.prep()

gene_dict = pcnode.run()[1]

meta = gene_dict['metadata']
genes = gene_dict['cluster']

res_dict = {}
for llm_use in [llm, llm_gpt]:
    for clu in genes.keys():
        cnode = CelltypeAnnoNode(llm_use, clu, genes[clu], meta['spec'], meta['tissue'])
        cnode.set_language(meta['language'])
        cnode.prep()
        res = cnode.run()

print(res_dict)
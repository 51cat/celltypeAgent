import pandas as pd
import requests
from typing import List, Dict


def collect_parms(p_type_column, cluster_column, gene_column, ntop, fc_column, spec, tissue, df = None, language ='中文'):
    """
        专门针对单细胞测序差异分析（DEG）结果设计的参数提取与基因筛选函数。

        参数 (Args):
        ----------
        p_type_column : str, default = 'p_val_adj'
            显著性指标列名用于初步过滤。
        cluster_column : str, default = 'cluster'
            分群信息列名。
        gene_column : str, default = 'gene'
            基因名称所在的列名
        ntop : int
            每个分群计划提取的 Top 基因数量。
        fc_column : str, default = 'avg_log2FC'
            用于排序的差异倍数列名
        spec : str
            物种元数据（例如 'Human', 'Mouse'），存入返回字典。
        tissue : str
            组织来源元数据（例如 'Liver', 'Brain'），存入返回字典。
        language: str, default: 中文
            交流语言选择

        返回 (Returns):
        -------
        dict
        """

    if isinstance(df, str):
        df = pd.read_csv(df)
    
    df_filtered = df[df[p_type_column] < 0.05].copy()
    
    top_genes = (
        df_filtered.groupby(cluster_column, group_keys=True)
        .apply(lambda x: x.nlargest(ntop, fc_column))
    ).reset_index()
    
    result = top_genes[[cluster_column, gene_column]]
    final_dict = result.groupby(cluster_column)[gene_column].apply(list).to_dict()
    final_dict_out = {}
    
    final_dict_out.update({"metadata":{"spec": spec, "tissue": tissue, "language": language}})
    final_dict_out.update({"cluster":final_dict})
    
    return final_dict_out
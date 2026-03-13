# 📊 细胞聚类自动注释分析报告 (Cluster 0)

## 1. 基本信息与共识结果
> 本部分概述该聚类在多模型分析下的身份认同感及结论可靠性。

* **Cluster ID**: 0
* **主要细胞类型 (Cell Type)**: T cells
* **细胞亚型 (Subcelltype)**: Naive / Central Memory T cells
* **共识达成情况**: ✅ 已达成共识 (比例: 1.0)
* **信息熵 (Entropy)**: 0.0 (数值越低一致性越高)
* **可靠性评估**: 均分 85.0 (gpt-5.4: 85, glm-5: 88, deepseek-v3.2: 82)

---

## 2. 关键特征基因 (Marker Genes)
> 基于高表达基因列表的生物学功能划分。

| 基因分类 | 标志性基因 | 生物学意义 |
| :--- | :--- | :--- |
| **谱系/定义 Marker** | `TRAT1`, `TCF7`, `LEF1`, `CCR7` | 明确支持该群属于 T 细胞谱系。`TRAT1` 指向 TCR 相关信号，`TCF7`/`LEF1` 为经典 T 细胞早期分化与稳态维持转录因子，`CCR7` 支持淋巴归巢型 T 细胞身份。 |
| **亚型特异 Marker** | `CCR7`, `TCF7`, `LEF1`, `MAL`, `TRABD2A` | 该组合高度符合初始型/低分化 T 细胞特征，常见于 Naive T cells 及 Central Memory T cells。`MAL` 和 `TRABD2A` 更偏向支持 naive 状态，但整体仍保留 naive 与 central memory 之间的连续谱特征。 |
| **功能/状态标志** | `IL6ST`, `MAL` | 提示该群细胞处于静息、未明显活化状态，未见显著增殖、应激或低质量信号。`IL6ST` 可作为辅助支持早期/稳态 T 细胞状态的证据。 |

---

## 3. 模型推理核心观点对比
> 展现不同 AI 模型在逻辑推演上的异同点。

### 🤖 gpt-5.4
* **核心定义**: Naive / central memory CD4+ T cells
* **逻辑**: 重点依据 `TRAT1`、`TCF7`、`LEF1`、`CCR7`、`MAL` 判断为典型 T 细胞，并进一步根据 `CCR7`、`TCF7`、`LEF1`、`TRABD2A`、`IL6ST` 的组合支持初始/中央记忆样状态。该模型倾向于将其解释为偏 CD4+ 的 naive/central memory T 细胞，但也承认缺乏更直接的 CD4 特异证据。

### 🎨 glm-5
* **核心定义**: Naive T cells
* **逻辑**: 以 `CCR7`、`LEF1`、`TCF7` 为核心证据，认为该 cluster 代表未分化、静息的初始 T 细胞，并结合 `MAL`、`TRABD2A` 进一步强化 naive 解释。该模型置信度最高，但也谨慎指出需与 Tcm 区分。

### 🧬 deepseek-v3.2
* **核心定义**: Naive T cells (Central Memory-like)
* **逻辑**: 同样基于 `LEF1`、`TCF7`、`CCR7`、`TRAT1` 确认 T 细胞谱系，并强调其具有未激活、归巢和自我更新相关特征，因此更倾向“naive 与 central memory 过渡样”解释。对于 `COL18A1` 等非典型信号，该模型采取保守处理，认为不足以推翻 T 细胞判断。

---

## 4. 审核意见与最终结论 (Audit Consensus)
> 结合顶级专家审核意见，对组织背景和模型偏倚进行最终校正。

> [!IMPORTANT]
> **最终鉴定结论：Naive / Central Memory T cells，整体处于静息、未明显活化状态。**

### 核心判定依据：
1. **基因保真度校核结果良好**: 三个模型均通过专家审核，`is_gene_faithful=True` 且 `is_biologically_valid=True`，未发现 gene hallucination，说明注释严格基于给定 marker gene。
2. **谱系与亚型证据高度一致**: `TRAT1`、`TCF7`、`LEF1`、`CCR7` 明确支持 T 细胞身份；`CCR7`、`TCF7`、`LEF1`、`MAL`、`TRABD2A` 共同支持 naive/Tcm 表型。由于缺乏足够强的单独证据将其稳定区分为纯 Naive 或纯 Central Memory，因此采用更稳健的合并亚型注释最合适。
3. **结论建议**: 后续若需进一步细分 Naive T cells 与 Central Memory T cells，建议结合 `IL7R`、`LTB`、`MAL`、`SELL`、`S100A4`、`MALAT1` 相关表达模式以及 CD4/CD8 分层信息，必要时联合 CITE-seq 或 TCR/clonotype 信息进行验证，以避免过度注释。
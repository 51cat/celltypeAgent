# 📊 细胞聚类自动注释分析报告 (Cluster 1)

## 1. 基本信息与共识结果
> 本部分概述该聚类在多模型分析下的身份认同感及结论可靠性。

* **Cluster ID**: 1
* **主要细胞类型 (Cell Type)**: Monocytes
* **细胞亚型 (Subcelltype)**: Classical Monocytes (Inflammatory)
* **共识达成情况**: ✅ 已达成共识 (比例: 0.67)
* **信息熵 (Entropy)**: 0.92 (数值越低一致性越高)
* **可靠性评估**: 均分 76.0 (gpt-5.4: 92, glm-5: 88, deepseek-v3.2: 48)

---

## 2. 关键特征基因 (Marker Genes)
> 基于高表达基因列表的生物学功能划分。

| 基因分类 | 标志性基因 | 生物学意义 |
| :--- | :--- | :--- |
| **谱系/定义 Marker** | `S100A8`, `S100A9`, `S100A12`, `PLBD1`, `BST1`, `CDA` | 共同指向髓系来源，且在 PBMC 背景下更符合经典单核细胞而非成熟中性粒细胞；其中 `S100A8/S100A9/S100A12` 为炎症性经典单核细胞核心标志组合。 |
| **亚型特异 Marker** | `S100A8`, `S100A9`, `S100A12`, `PLBD1`, `BST1` | 支持 Classical Monocytes，尤其是 CD14样、炎症偏向亚群；该组合在外周血经典单核细胞中较常见。 |
| **功能/状态标志** | `PADI4`, `NLRP12`, `CYP27A1`, `RBP7` | 提示先天免疫激活与炎症反应状态，支持该群细胞处于 inflammatory/activated 状态，而非增殖群或低质量细胞。 |

---

## 3. 模型推理核心观点对比
> 展现不同 AI 模型在逻辑推演上的异同点。

### 🤖 gpt-5.4
* **核心定义**: Myeloid cells → Classical monocytes / inflammatory monocytes
* **逻辑**: 重点依据 `S100A8/S100A9/S100A12`、`PLBD1`、`BST1`、`CDA` 等髓系与单核细胞相关标志，将该群判定为 PBMC 中的炎症性经典单核细胞；同时认为 `PADI4`、`NLRP12` 反映先天免疫活化状态。

### 🎨 glm-5
* **核心定义**: Monocytes → Classical Monocytes
* **逻辑**: 强调 `S100A8/S100A9/S100A12` 在 PBMC 样本中对经典单核细胞的支持作用，并结合 Ficoll 分离背景，认为成熟中性粒细胞大量出现的可能性较低；`BST1`、`PLBD1` 进一步支持单核细胞注释。

### ⚠️ deepseek-v3.2
* **核心定义**: Neutrophils → Activated / Inflammatory Neutrophils
* **逻辑**: 将 `S100A8/S100A9/S100A12` 与 `PADI4`、`PLBD1` 的组合优先解释为中性粒细胞特征，认为该群属于活化炎症性中性粒细胞；但该解释未充分结合 PBMC 制备背景，生物学合理性不足。

---

## 4. 审核意见与最终结论 (Audit Consensus)
> 结合顶级专家审核意见，对组织背景和模型偏倚进行最终校正。

> [!IMPORTANT]
> **最终鉴定结论：Classical Monocytes (Inflammatory)，即炎症性经典单核细胞。**

### 核心判定依据：
1. **基因保真度与高可信模型一致性**: 三个模型引用基因均来自给定 Marker Gene List，不存在 Gene Hallucination；其中 gpt-5.4 与 glm-5 均通过生物学有效性审核，且可靠性评分高（92、88），一致支持单核细胞结论。
2. **组织背景校正后的谱系判定**: 虽然 `S100A8/S100A9/S100A12` 与 `PADI4` 也可见于粒细胞，但在标准 Ficoll 制备的 PBMC 语境下，成熟中性粒细胞通常被去除，因此该 cluster 更合理解释为经典单核细胞，且带有明显炎症活化特征。
3. **结论建议**: 后续分析中建议将该群作为 **CD14+ classical/inflammatory monocyte** 纳入髓系重分析；可结合 `LYZ`、`FCN1`、`CTSS`、`SAT1`、`VCAN`、`FCGR3A` 等单核细胞分层标记进一步验证其与非经典单核细胞、低密度粒细胞之间的边界。
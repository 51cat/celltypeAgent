# CelltypeAgent

一个基于多模型细胞类型注释的多agent协作系统，用于单细胞RNA测序数据的自动细胞类型注释。

## 项目目的

1. 开发一个基于多模型细胞类型注释的多agent协作系统
2. 不调用任何框架，例如langchain，从零实现，主要目的是学习
3. 长远目标，未来可以部署到自己的云服务器

## 功能特性

- 多LLM模型支持（GPT、Claude、MiniMax、Qwen等）
- 自动参数收集和细胞类型注释
- 并行处理多个簇（clusters）
- 支持多种物种和组织类型
- 详细的推理过程记录

## 安装

...

## 项目结构

```
celltypeAgent/
├── agent.py              # 主程序入口
├── config.json           # 配置文件
├── llm/                  # LLM接口模块
├── nodes/                # 节点模块（参数收集、注释、审核）
├── prompt/               # 提示模板
└── tools/                # 工具函数
```

## 依赖

- requests
- pandas
- openai
- openpyxl (可选，用于Excel文件处理)

## 参考

- [DeepSearchAgent-Demo](https://github.com/666ghj/DeepSearchAgent-Demo)
# 科研方向助手（Research Helper）

## 项目简介

科研方向助手是一个智能科研辅助工具，旨在帮助研究人员高效收集领域论文、管理文献资源并生成有针对性的科研方向建议。该工具通过爬虫技术从权威学术平台获取最新研究论文，利用向量数据库进行高效存储和检索，并结合大语言模型为用户提供个性化的科研指导。

## 核心功能

### 1. 智能论文收集
- 支持从 arXiv 和 ACL Anthology 两个权威学术平台抓取论文
- 可通过关键词或自然语言描述自动分析并抓取相关领域论文
- 支持自定义抓取数量和排序方式（相关度或最新）
- 自动分类存储 PDF 论文文件

### 2. 向量数据库管理
- 使用 ChromaDB 构建论文向量数据库
- 支持增量更新和全量更新
- 高效的文本嵌入和相似性检索
- 支持按关键词筛选更新范围

### 3. 科研建议生成
- 基于收集的论文内容生成个性化科研建议
- 支持对话历史记录管理
- 可通过对话 ID 恢复历史会话
- 结合大语言模型提供深入的学术分析

### 4. API 服务支持
- 提供 RESTful API 接口
- 支持论文收集、数据库更新等操作
- 方便集成到其他科研工作流中

## 项目结构

```
ResearchHelper/
├── config/                        # 配置管理
│   └── settings.py                # 项目配置文件
├── src/                           # 核心源代码
│   ├── crawlers/                  # 爬虫模块
│   │   ├── __init__.py            # 爬虫模块初始化
│   │   ├── base_crawler.py        # 爬虫基类
│   │   ├── arxiv_crawler.py       # arXiv爬虫实现
│   │   └── aclanthology_crawler.py # ACL anthology爬虫实现
│   ├── api_client.py              # API客户端封装
│   ├── generate_answer.py         # 科研建议生成
│   └── update_vector_db.py        # 向量数据库更新
├── storage/                       # 数据存储目录
│   ├── papers/                    # PDF论文存储（按主题分类）
│   │   └── [主题名称]/            # 自动创建的主题文件夹
│   │       ├── chroma_db/         # 该主题的向量数据库
│   │       └── *.pdf              # 收集的PDF论文
│   └── history_chat/              # 对话历史记录（JSON格式）
├── app.py                         # Flask API服务入口
├── main.py                        # 命令行工具入口
├── requirements.txt               # 项目依赖
├── research_helper.log            # 日志文件
└── test.py                        # 测试文件
```

## 技术栈

| 类别 | 技术/库 | 用途 |
|------|---------|------|
| 编程语言 | Python 3.8+ | 项目主要开发语言 |
| 爬虫框架 | BeautifulSoup4, Selenium | 学术论文抓取 |
| 向量数据库 | ChromaDB | 论文内容存储与检索 |
| 大语言模型接口 | OpenAI API 兼容接口 | 对话生成与关键词推断 |
| 嵌入模型 | BAAI/bge-m3 | 文本向量化 |
| Web 框架 | Flask | API 服务提供 |
| PDF 处理 | PyMuPDF | PDF 文本提取 |

## 安装与配置

### 1. 环境要求

- Python 3.8 或更高版本
- Windows/macOS/Linux 操作系统

### 2. 安装依赖

```bash
# macOS 用户需要额外安装工具包
pip install tools==0.1.9

# 安装核心依赖
pip install -r requirements.txt
```

### 3. 配置设置

在 `config/settings.py` 文件中配置以下参数：

```python
# 大模型 API 配置
API_KEY = "sk-xxx"  # 替换为你的 API Key
BASE_URL = "https://api.siliconflow.cn/v1"  # API 基础 URL
CHAT_MODEL = "deepseek-ai/DeepSeek-R1"  # 对话模型
EMBEDDING_MODEL = "BAAI/bge-m3"  # 嵌入模型

# 对话生成配置
MAX_TOKEN = 2048  # 最大生成 token 数
TEMPERATURE = 0.7  # 生成温度

# 检索配置
TOP_K = 10  # 检索相关文档数量

# 爬虫配置
CRAWL_DELAY = 1  # 爬虫延迟（秒）
DOWNLOAD_RETRIES = 3  # 下载重试次数
```

## 使用方法

### 1. 命令行工具

#### 收集论文

```bash
# 通过关键词收集论文
python main.py collect --keywords "large language models" --max 5

# 通过自然语言描述收集论文
python main.py collect --description "大模型相关领域的方向" --max 3

# 指定数据源为 ACL（默认 arXiv）
python main.py collect --keywords "NLP" --source acl --max 10

# 按最新排序收集论文
python main.py collect --keywords "computer vision" --sort latest --max 5
```

#### 更新向量数据库

```bash
# 更新指定关键词的向量数据库
python main.py update_db --keywords "large language models"

# 更新所有向量数据库
python main.py update_db
```

#### 生成科研建议

```bash
# 发起新的科研建议请求
python main.py advise --keywords "large language models" --query "我手头的算力资源并不充裕，从科研的角度来讲，我可以在哪些大模型的方向进行尝试呢？"

# 基于历史对话 ID 继续对话
python main.py advise --keywords "large language models" --id 1
```

### 2. API 服务

#### 启动 API 服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

#### API 接口说明

##### 收集论文

```bash
POST /api/collect
Content-Type: application/json

{
  "keywords": ["large language models", "transformer"],
  "max": 5,
  "source": "arxiv",
  "sort": "relevance"
}
```

或通过描述自动推断关键词：

```bash
POST /api/collect
Content-Type: application/json

{
  "description": "大模型相关领域的最新研究",
  "max": 3,
  "source": "arxiv"
}
```

##### 更新向量数据库

```bash
POST /api/update_db
Content-Type: application/json

{
  "keywords": "large language models"
}
```

## 工作流程

1. **论文收集**：
   - 用户通过关键词或描述指定研究领域
   - 系统使用相应的爬虫从学术平台抓取论文
   - 论文自动分类存储到 `storage/papers/[主题名称]/` 目录

2. **向量数据库构建**：
   - 提取论文文本内容
   - 使用嵌入模型将文本转换为向量
   - 将向量存储到 ChromaDB 中

3. **科研建议生成**：
   - 用户提出科研相关问题
   - 系统从向量数据库中检索相关论文
   - 结合大语言模型生成个性化科研建议
   - 对话历史存储到 `storage/history_chat/` 目录

## 配置说明

### 核心配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| API_KEY | 大语言模型 API 密钥 | - |
| BASE_URL | API 基础 URL | https://api.siliconflow.cn/v1 |
| CHAT_MODEL | 对话生成模型 | deepseek-ai/DeepSeek-R1 |
| EMBEDDING_MODEL | 文本嵌入模型 | BAAI/bge-m3 |
| MAX_TOKEN | 最大生成 token 数 | 2048 |
| TEMPERATURE | 生成温度 | 0.7 |
| TOP_K | 检索相关文档数量 | 10 |
| CRAWL_DELAY | 爬虫延迟（秒） | 1 |

### 调整建议

- 如果生成的建议被截断，可增大 `MAX_TOKEN` 值
- 若需要更准确的建议，可降低 `TEMPERATURE` 值
- 如需更全面的检索结果，可调整 `TOP_K` 值
- 若爬虫过程中遇到访问限制，可增大 `CRAWL_DELAY` 值

## 注意事项

1. **API 密钥安全**：请妥善保管你的 API 密钥，避免泄露
2. **爬虫合规性**：请遵守各学术平台的爬虫规则，合理设置抓取频率
3. **存储空间**：随着论文数量增加，需确保有足够的存储空间
4. **网络环境**：确保网络连接稳定，尤其是在大规模抓取论文时
5. **依赖更新**：定期更新依赖库以获得更好的性能和安全性

## 日志管理

系统日志存储在 `research_helper.log` 文件中，包含：
- 论文收集过程日志
- 数据库更新日志
- 对话生成日志
- 错误信息记录

可通过日志文件跟踪系统运行状态和排查问题。

## 扩展建议

1. 添加更多学术平台支持（如 IEEE Xplore、SpringerLink 等）
2. 实现论文自动摘要功能
3. 支持更多格式的文献导入导出
4. 添加可视化分析功能，展示领域研究趋势
5. 实现多语言支持

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进项目！

## 联系方式

如有问题或建议，欢迎通过以下方式联系：
- 邮箱：[your-email@example.com]
- GitHub：[your-github-repo]

---

**使用科研方向助手，让你的科研之路更加高效！**
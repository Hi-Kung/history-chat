# ⚔️ 历史人物对话

> 穿越时空，与历史人物面对面 —— 基于大语言模型的沉浸式历史人物对话应用

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 项目简介

**历史人物对话**是一款基于 Streamlit 构建的交互式 Web 应用，接入 SiliconFlow 提供的 DeepSeek-V3 大语言模型，让用户能够以自然语言与中国历史名人展开对话。每位人物都有独特的性格设定与说话风格，力求还原历史人物的精神气质。

---

## ✨ 功能特性

- 🧠 **5 位历史人物** — 诸葛亮、武则天、苏轼、岳飞、王阳明，各具鲜明人格
- 💬 **流式输出** — 逐字显示回复，对话体验流畅自然
- 🎛️ **创意程度调节** — 通过滑块控制模型温度（0.0 ~ 1.0）
- 🪟 **滑动上下文窗口** — 自动保留最近 8 轮对话，防止 Token 超限
- 💡 **提示问题引导** — 每位人物预设 4 个经典问题，一键发起对话
- 🔄 **人物切换自动清空** — 切换人物时自动重置会话，避免上下文混乱
- 📥 **聊天记录下载** — 支持将对话导出为 `.txt` 文件
- 🖼️ **人物头像展示** — 侧边栏展示自定义人物头像图片

---

## 🧑‍🤝‍🧑 支持的历史人物

| 人物 | 朝代 | 特色风格 |
|------|------|----------|
| 🪁 诸葛亮 | 三国·蜀汉 | 文言文风格，沉稳睿智 |
| 👑 武则天 | 唐朝 | 帝王口吻，自信强势 |
| 🖌️ 苏轼 | 北宋 | 幽默风趣，引用诗词 |
| ⚔️ 岳飞 | 南宋 | 坚定悲壮，精忠报国 |
| 🧘 王阳明 | 明朝 | 深沉睿智，知行合一 |

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/historical-chat.git
cd historical-chat
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**`requirements.txt` 参考内容：**

```
streamlit>=1.30.0
openai>=1.0.0
```

### 3. 配置 API Key

本项目使用 [SiliconFlow](https://siliconflow.cn) 提供的 API 服务。请先注册账号并获取 API Key，然后设置环境变量：

```bash
# Linux / macOS
export SILICONFLOW_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:SILICONFLOW_API_KEY="your_api_key_here"
```

或在项目根目录创建 `.env` 文件（需配合 `python-dotenv` 使用）：

```
SILICONFLOW_API_KEY=your_api_key_here
```

### 4. 准备头像资源（可选）

在项目根目录下创建头像目录，并放入对应图片：

```
assets/
└── avatars/
    ├── zhuge_liang.png
    ├── wu_zetian.png
    ├── su_shi.png
    ├── yue_fei.png
    └── wang_yangming.png
```

> 若未找到头像文件，应用会显示提示信息但不影响正常使用。

### 5. 启动应用

```bash
streamlit run app.py
```

浏览器访问 `http://localhost:8501` 即可开始对话。

---

## 📁 项目结构

```
historical-chat/
├── app.py                  # 主应用入口
├── requirements.txt        # 依赖列表
├── README.md               # 项目说明
└── assets/
    └── avatars/            # 人物头像图片目录
        ├── zhuge_liang.png
        ├── wu_zetian.png
        ├── su_shi.png
        ├── yue_fei.png
        └── wang_yangming.png
```

---

## ⚙️ 配置说明

| 参数 | 位置 | 说明 |
|------|------|------|
| `MAX_TURNS` | `app.py` | 滑动窗口保留的最大对话轮数，默认 `8` |
| `model` | `app.py` | 调用的模型名称，默认 `deepseek-ai/DeepSeek-V3` |
| `max_tokens` | `app.py` | 单次回复最大 Token 数，默认 `600` |
| `temperature` | 侧边栏滑块 | 模型创意程度，范围 0.0 ~ 1.0，推荐 0.7 ~ 0.9 |

---

## 🔧 扩展与自定义

### 添加新历史人物

在 `app.py` 的 `CHARACTERS` 字典中添加新条目：

```python
CHARACTERS['新人物名'] = {
    'prompt': '角色扮演提示词，描述人物性格、说话风格等',
    'intro': '人物简介，显示在侧边栏',
    'emoji': '🏮',
    'avatar': 'new_character.png',
}
```

同时在 `HINT_QUESTIONS` 中添加对应的提示问题：

```python
HINT_QUESTIONS['新人物名'] = ['问题一？', '问题二？', '问题三？', '问题四？']
```

### 更换模型

修改 `app.py` 中的 `model` 参数为 SiliconFlow 平台支持的其他模型：

```python
model='Qwen/Qwen2.5-72B-Instruct'  # 替换为其他模型
```

---

## 📄 License

本项目基于 [MIT License](LICENSE) 开源，欢迎自由使用与二次开发。

---

## 🙏 致谢

- [SiliconFlow](https://siliconflow.cn) — 提供大模型 API 服务
- [DeepSeek](https://deepseek.com) — 底层语言模型
- [Streamlit](https://streamlit.io) — 快速构建 Web 应用框架

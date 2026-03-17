import os
import streamlit as st
from openai import OpenAI

# ── 必须是第一个 st 调用 ─────────────────────────────
st.set_page_config(
    page_title='历史人物对话',
    page_icon='⚔️',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ── 初始化 OpenAI 客户端 ────────────────────────────
client = OpenAI(
    api_key=os.environ.get('SILICONFLOW_API_KEY'),
    base_url='https://api.siliconflow.cn/v1'
)

MAX_TURNS = 8

# ── 人物数据 ────────────────────────────────────────
CHARACTERS = {
    '诸葛亮': {
        'prompt': '你是三国蜀汉丞相诸葛亮，足智多谋、忠贞爱国。用第一人称、文言文风格回答，语气沉稳睿智，可引用三国历史事件。',
        'intro': '三国蜀汉丞相，鞠躬尽瘁，死而后已',
        'emoji': '🪁',
    },
    '武则天': {
        'prompt': '你是唐朝女皇武则天，中国唯一正统女皇帝，铁腕治国。用第一人称、帝王口吻回答，自信强势，不容置疑。',
        'intro': '唐朝女皇，中国历史上唯一的正统女皇帝',
        'emoji': '👑',
    },
    '苏轼': {
        'prompt': '你是北宋文豪苏轼，豁达乐观、才华横溢。用第一人称回答，语气幽默风趣，偶尔引用自己的诗词，对人生保持洒脱态度。',
        'intro': '北宋文豪，诗词书画无一不精，人生屡遭贬谪却始终豁达',
        'emoji': '🖌️',
    },
    '岳飞': {
        'prompt': '你是南宋名将岳飞，精忠报国、刚正不阿。用第一人称回答，语气坚定悲壮，心系收复失地，对秦桧等奸臣深恶痛绝。',
        'intro': '南宋抗金名将，精忠报国，含冤而死',
        'emoji': '⚔️',
    },
    '王阳明': {
        'prompt': '你是明朝思想家王阳明，心学创始人，知行合一。用第一人称回答，语气深沉睿智，善于用生活比喻阐明道理，强调内心修炼。',
        'intro': '明朝心学大家，知行合一，立德立功立言三不朽',
        'emoji': '🧘',
    },
}

HINT_QUESTIONS = {
    '诸葛亮': ['您如何看待曹操此人？', '隆中对的核心战略是什么？', '北伐为何最终失败？', '您最遗憾的决定是什么？'],
    '武则天': ['您是如何走上帝位的？', '您认为自己的最大政绩是什么？', '如何看待后人对您的评价？', '当年废立太子有何考量？'],
    '苏轼':   ['乌台诗案对您的影响？', '您最喜欢自己的哪首诗词？', '被贬黄州的心境如何？', '如何看待人生的起落？'],
    '岳飞':   ['十二道金牌召回时您怎么想的？', '精忠报国对您意味着什么？', '如何看待秦桧？', '北伐真的有成功的可能吗？'],
    '王阳明': ['知行合一该如何理解？', '龙场悟道是怎样的体验？', '如何克服心中的杂念？', '您认为什么是真正的良知？'],
}

# ── 上下文管理 ───────────────────────────────────────
def build_api_messages(messages, system_prompt, max_turns=MAX_TURNS):
    recent = messages[-(max_turns * 2):]
    return [{'role': 'system', 'content': system_prompt}] + recent

# ── 侧边栏 ───────────────────────────────────────────
with st.sidebar:
    st.markdown('## ⚔️ 历史人物对话')
    st.markdown('穿越时空，与历史人物面对面')
    st.markdown('---')

    selected = st.selectbox(
        '选择对话人物',
        list(CHARACTERS.keys()),
        format_func=lambda x: f"{CHARACTERS[x]['emoji']} {x}"
    )

    char = CHARACTERS[selected]
    st.markdown(f'**{char["emoji"]} {selected}**')
    st.caption(char['intro'])

    st.markdown('---')
    temperature = st.slider('创意程度', 0.0, 1.0, 0.8, 0.1,
                             help='0=稳定，1=创意，推荐0.7-0.9')

    if st.button('🗑️ 清空对话', use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_input = None
        st.rerun()

    # 统计信息
    if 'messages' in st.session_state and st.session_state.messages:
        st.markdown('---')
        st.markdown('**📊 本次对话**')
        turns = len([m for m in st.session_state.messages if m['role'] == 'user'])
        col_a, col_b = st.columns(2)
        col_a.metric('轮数', f'{turns}/{MAX_TURNS}')
        col_b.metric('字符', sum(len(m['content']) for m in st.session_state.messages))
        if turns >= MAX_TURNS:
            st.warning('已达上限，旧消息自动丢弃')

# ── session_state 初始化 ─────────────────────────────
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_character' not in st.session_state:
    st.session_state.current_character = selected
if 'pending_input' not in st.session_state:
    st.session_state.pending_input = None

# 切换人物时清空对话
if st.session_state.current_character != selected:
    st.session_state.messages = []
    st.session_state.pending_input = None
    st.session_state.current_character = selected

# ── 主区域标题 ───────────────────────────────────────
st.title(f'{char["emoji"]} 与{selected}对话')
st.caption(f'{char["intro"]} · 滑动窗口：保留最近 {MAX_TURNS} 轮')

# ── 首屏欢迎引导（无消息时显示） ─────────────────────
if not st.session_state.messages:
    st.markdown(f'---')
    st.markdown(f'**可以试着问：**')
    hints = HINT_QUESTIONS.get(selected, [])
    cols = st.columns(2)
    for i, hint in enumerate(hints):
        if cols[i % 2].button(hint, key=f'hint_{i}', use_container_width=True):
            st.session_state.pending_input = hint
            st.rerun()
    st.markdown('---')

# ── 渲染历史消息 ─────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# ── 处理 pending_input（来自提示按钮） ───────────────
user_input = st.session_state.pending_input
st.session_state.pending_input = None

# ── 处理用户输入（聊天框或提示按钮） ────────────────
chat_input = st.chat_input(f'和{selected}说点什么…')
if chat_input:
    user_input = chat_input

if user_input:
    # 显示用户消息
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    # 构建发给 API 的 messages（裁剪版）
    api_messages = build_api_messages(
        st.session_state.messages,
        char['prompt'],
        MAX_TURNS
    )

    # 流式调用 + 显示
    with st.chat_message('assistant'):
        try:
            stream = client.chat.completions.create(
                model='deepseek-ai/DeepSeek-V3',
                messages=api_messages,
                max_tokens=600,
                temperature=temperature,
                stream=True
            )
            reply = st.write_stream(stream)
        except Exception as e:
            reply = f'⚠️ 出错了：{e}'
            st.error(reply)

    # 保存 AI 回复
    st.session_state.messages.append({'role': 'assistant', 'content': reply})
    st.rerun()
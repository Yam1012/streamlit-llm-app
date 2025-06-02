import streamlit as st

# ✅ 最初に1回だけ呼び出す（他の st. コマンドの前に）
st.set_page_config(page_title="専門家チャット", layout="centered")

from dotenv import load_dotenv
load_dotenv()

from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# OpenAI APIキーの取得
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を設定してください。")
    st.stop()

# 専門家のプロンプトを返す関数
def get_system_prompt(expert_type):
    if expert_type == "医者":
        return "あなたは経験豊富な日本の医師です。ユーザーの健康に関する質問に対して、わかりやすく丁寧に答えてください。"
    elif expert_type == "弁護士":
        return "あなたは日本の法律に精通した弁護士です。法的な質問に対して、専門的かつ分かりやすく回答してください。"
    else:
        return "あなたは有能な一般アシスタントです。ユーザーの質問に対して誠実に対応してください。"

# ChatOpenAI インスタンスを作成
chat = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

# ユーザー入力と専門家種別をもとに LLM に問い合わせ
def ask_expert(user_input, expert_type):
    messages = [
        SystemMessage(content=get_system_prompt(expert_type)),
        HumanMessage(content=user_input)
    ]
    response = chat(messages)
    return response.content

# --- Streamlit UI ---

st.title("🧠 専門家に聞いてみよう！")
st.write("""
このアプリでは、質問内容に応じて「医者」「弁護士」または「一般アシスタント」の専門家を選び、
AIがその分野の専門家として回答してくれます。

**使い方：**
1. 専門家の種類を選択してください。
2. 質問を入力して「送信」ボタンを押してください。
""")

# 専門家の選択
expert_type = st.selectbox("専門家の種類を選択してください", ["医者", "弁護士", "一般"])

# ユーザーの質問入力
user_input = st.text_area("質問を入力してください", "")

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("考え中..."):
            response = ask_expert(user_input, expert_type)
            st.success("回答：")
            st.write(response)

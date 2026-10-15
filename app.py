import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="مساعدي الذكي", page_icon="🤖")
st.title("🤖 مساعدي الذكي - Groq")

# قائمة النماذج المتاحة على Groq
AVAILABLE_MODELS = [
    {"name": "Llama 3.3 70B (الأقوى)", "id": "llama-3.3-70b-versatile"},
    {"name": "Llama 3.1 8B (الأسرع)", "id": "llama-3.1-8b-instant"},
    {"name": "Mixtral 8x7B (متوازن)", "id": "mixtral-8x7b-32768"},
    {"name": "Gemma 2 9B (من جوجل)", "id": "gemma2-9b-it"},
]

model_choice = st.selectbox("اختر نموذج الذكاء الاصطناعي:", [m["name"] for m in AVAILABLE_MODELS])
selected_model_id = next(m["id"] for m in AVAILABLE_MODELS if m["name"] == model_choice)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"جاري التفكير باستخدام {model_choice}..."):
            try:
                response = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model=selected_model_id,
                    max_tokens=800
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"صار خطأ: {e}")

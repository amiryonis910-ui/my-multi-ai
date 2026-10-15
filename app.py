import streamlit as st
from huggingface_hub import InferenceClient
import io

# الاتصال بـ Hugging Face
client = InferenceClient(token=st.secrets["HF_TOKEN"])

st.set_page_config(page_title="مساعدي الذكي الشامل", page_icon="🚀", layout="wide")
st.title("🚀 مساعدي الذكي الشامل - كل شي في مكان واحد")

# إنشاء التبويبات
tab1, tab2, tab3, tab4 = st.tabs(["💬 محادثة", "🎨 توليد صور", "🎵 تحويل نص لصوت", "🎬 توليد فيديو"])

# ==========================================
# 1. تبويب المحادثة (Chat)
# ==========================================
with tab1:
    st.header("💬 محادثة ذكية")
    
    chat_models = [
        {"name": "Qwen 2.5 7B (متوازن)", "id": "Qwen/Qwen2.5-7B-Instruct"},
        {"name": "Mistral 7B (سريع)", "id": "mistralai/Mistral-7B-Instruct-v0.3"},
        {"name": "Zephyr 7B (محادثة)", "id": "HuggingFaceH4/zephyr-7b-beta"},
    ]
    
    chat_model_choice = st.selectbox("اختر نموذج المحادثة:", [m["name"] for m in chat_models])
    chat_model_id = next(m["id"] for m in chat_models if m["name"] == chat_model_choice)

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
            with st.spinner("جاري التفكير..."):
                try:
                    response = client.chat_completion(
                        messages=st.session_state.messages,
                        model=chat_model_id,
                        max_tokens=800
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"عذراً، صار خطأ: {e}. جرب نموذج ثاني أو انتظر شوي.")

# ==========================================
# 2. تبويب توليد الصور (Text-to-Image)
# ==========================================
with tab2:
    st.header("🎨 توليد صور من النص")
    st.write("اكتب وصف الصورة بالانجليزي عشان تكون النتيجة أدق.")
    
    image_models = [
        {"name": "FLUX.1-schnell (سريع جداً)", "id": "black-forest-labs/FLUX.1-schnell"},
        {"name": "Stable Diffusion XL", "id": "stabilityai/stable-diffusion-xl-base-1.0"},
    ]
    
    image_model_choice = st.selectbox("اختر نموذج الصور:", [m["name"] for m in image_models])
    image_model_id = next(m["id"] for m in image_models if m["name"] == image_model_choice)
    
    image_prompt = st.text_input("وصف الصورة:", placeholder="A cute cat wearing a crown, digital art")
    
    if st.button("🎨 ولد الصورة"):
        if image_prompt:
            with st.spinner("جاري رسم الصورة... قد يأخذ بعض الوقت ⏳"):
                try:
                    image = client.text_to_image(image_prompt, model=image_model_id)
                    st.image(image, caption="هذي هي صورتك! ✨", use_column_width=True)
                except Exception as e:
                    st.error(f"عذراً، فشل توليد الصورة: {e}")
        else:
            st.warning("اكتب وصف أول!")

# ==========================================
# 3. تبويب الصوت (Text-to-Speech)
# ==========================================
with tab3:
    st.header("🎵 تحويل النص إلى صوت")
    st.write("اكتب أي نص (يفضل انجليزي لأن النماذج المجانية تدعمه بشكل أفضل).")
    
    tts_text = st.text_area("النص:", placeholder="Hello, this is my AI assistant speaking.")
    
    if st.button("🎵 حول لصوت"):
        if tts_text:
            with st.spinner("جاري توليد الصوت... ⏳"):
                try:
                    audio_bytes = client.text_to_speech(tts_text, model="suno/bark-small")
                    st.audio(audio_bytes, format="audio/wav")
                    st.success("تم توليد الصوت بنجاح! 🎧")
                except Exception as e:
                    st.error(f"عذراً، فشل توليد الصوت: {e}")
        else:
            st.warning("اكتب نص أول!")

# ==========================================
# 4. تبويب الفيديو (Text-to-Video)
# ==========================================
with tab4:
    st.header("🎬 توليد فيديو من النص")
    st.write("⚠️ تنبيه: توليد الفيديو على الخطة المجانية بطيء جداً وقد يفشل بسبب ضغط السيرفرات. جربه بصبر.")
    
    video_prompt = st.text_input("وصف الفيديو:", placeholder="A astronaut walking on the moon")
    
    if st.button("🎬 ولد الفيديو"):
        if video_prompt:
            with st.spinner("جاري توليد الفيديو... هذا قد يأخذ دقائق ⏳"):
                try:
                    video_bytes = client.text_to_video(video_prompt, model="damo-vilab/text-to-video-ms-1.7b")
                    st.video(video_bytes)
                    st.success("تم توليد الفيديو! 🎥")
                except Exception as e:
                    st.error(f"عذراً، فشل توليد الفيديو: {e}. الخطة المجانية ما تكفي لهذي النماذج غالباً.")
        else:
            st.warning("اكتب وصف أول!")

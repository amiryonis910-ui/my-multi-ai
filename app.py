import streamlit as st
import requests
from groq import Groq
from magic_hour import Client
import os

# ---------------------------------------------
# إعدادات الاتصال بمزودي الخدمة
# ---------------------------------------------

# 1. عميل Groq (للنصوص)
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"خطأ في إعداد مفتاح Groq: {e}")
    groq_client = None

# 2. عميل Magic Hour (للفيديو)
try:
    magic_hour_client = Client(token=st.secrets["MAGIC_HOUR_API_KEY"])
except Exception as e:
    st.error(f"خطأ في إعداد مفتاح Magic Hour: {e}")
    magic_hour_client = None

# ---------------------------------------------
# إعدادات الواجهة
# ---------------------------------------------
st.set_page_config(page_title="استوديو الذكاء الاصطناعي", page_icon="🎨", layout="wide")
st.title("🎨 استوديو الذكاء الاصطناعي - نصوص، صور، فيديو")

tab1, tab2, tab3 = st.tabs(["💬 محادثة (Groq)", "🎨 توليد صور (Pollinations)", "🎬 توليد فيديو (Magic Hour)"])

# ==========================================
# 1. تبويب المحادثة (النصوص) - باستخدام Groq
# ==========================================
with tab1:
    st.header("💬 محادثة ذكية")
    st.write("محادثة فائقة السرعة باستخدام نماذج Llama من Groq.")

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
                    if groq_client:
                        response = groq_client.chat.completions.create(
                            messages=st.session_state.messages,
                            model="llama-3.3-70b-versatile",
                            max_tokens=1024
                        )
                        reply = response.choices[0].message.content
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    else:
                        st.error("عميل Groq غير مهيأ. تأكد من إضافة GROQ_API_KEY في إعدادات الأسرار.")
                except Exception as e:
                    st.error(f"عذراً، حدث خطأ: {e}")

# ==========================================
# 2. تبويب توليد الصور - باستخدام Pollinations.ai
# ==========================================
with tab2:
    st.header("🎨 توليد صور من النص")
    st.write("اكتب وصفًا تفصيليًا باللغة الإنجليزية للحصول على أفضل النتائج.")
    
    image_prompt = st.text_area(
        "وصف الصورة:",
        placeholder="A majestic lion wearing a golden crown, digital art, hyper-realistic, 8k",
        height=100
    )
    
    if st.button("🎨 توليد الصورة", type="primary"):
        if image_prompt:
            with st.spinner("جاري رسم الصورة... قد يستغرق هذا بضع ثوانٍ ⏳"):
                try:
                    # استخدام واجهة برمجة تطبيقات Pollinations.ai
                    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_prompt)}?width=1024&height=1024&nologo=true"
                    response = requests.get(url, timeout=60)
                    
                    if response.status_code == 200:
                        st.image(response.content, caption="النتيجة", use_column_width=True)
                    else:
                        st.error(f"فشل توليد الصورة. رمز الحالة: {response.status_code}")
                except Exception as e:
                    st.error(f"عذراً، فشل توليد الصورة: {e}")
        else:
            st.warning("الرجاء كتابة وصف أولاً!")

# ==========================================
# 3. تبويب توليد الفيديو - باستخدام Magic Hour
# ==========================================
with tab3:
    st.header("🎬 توليد فيديو من النص")
    st.write("أنشئ فيديو قصيرًا من وصف نصي. توليد الفيديو قد يستغرق بعض الوقت.")
    
    video_prompt = st.text_area(
        "وصف الفيديو:",
        placeholder="A serene beach at sunset with gentle waves and a flying seagull",
        height=100
    )
    
    if st.button("🎬 توليد الفيديو", type="primary"):
        if video_prompt:
            with st.spinner("جاري توليد الفيديو... قد يستغرق هذا من 30 ثانية إلى دقيقتين ⏳"):
                try:
                    if magic_hour_client:
                        # استدعاء Magic Hour API لتوليد الفيديو
                        result = magic_hour_client.v1.text_to_video.generate(
                            end_seconds=5.0,
                            aspect_ratio="16:9",
                            model="wan-2.2",  # نموذج مجاني
                            prompt=video_prompt
                        )
                        
                        if result and result.get("status") == "complete":
                            video_url = result.get("video_url")
                            st.success("تم توليد الفيديو بنجاح! 🎉")
                            st.video(video_url)
                        else:
                            st.warning("لم يكتمل توليد الفيديو. قد يكون الرصيد غير كافٍ أو حدث خطأ.")
                    else:
                        st.error("عميل Magic Hour غير مهيأ. تأكد من إضافة MAGIC_HOUR_API_KEY في إعدادات الأسرار.")
                except Exception as e:
                    st.error(f"عذراً، فشل توليد الفيديو: {e}")
        else:
            st.warning("الرجاء كتابة وصف أولاً!")

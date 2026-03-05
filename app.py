import streamlit as st
import google.generativeai as genai

st.title("🎓 Генератор планов")

# Проверка ключа
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Ошибка: Перейди в Settings -> Secrets и добавь GOOGLE_API_KEY")
    st.stop()

# Настройка
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Используем gemini-1.5-pro (она чаще доступна, чем flash)
model = genai.GenerativeModel('gemini-1.5-pro')

topic = st.text_input("Тема урока")

if st.button("Сгенерировать"):
    if topic:
        with st.spinner('Генерирую...'):
            try:
                response = model.generate_content(f"Составь план урока на тему: {topic}")
                st.write(response.text)
            except Exception as e:
                st.error(f"Ошибка API: {e}")

import streamlit as st
import google.generativeai as genai
import io
from docx import Document

# 1. Настройка страницы
st.set_page_config(page_title="Конструктор КСП", layout="wide")
st.title("🎓 Конструктор КСП")

# 2. Безопасная инициализация
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Ключ не найден в Secrets!")
    st.stop()

# 3. Настройка клиента API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Вместо того чтобы спрашивать список моделей, мы сразу указываем рабочую
# Если gemini-1.5-flash не работает, поменяй на 'gemini-1.5-pro'
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Интерфейс
with st.sidebar:
    fio = st.text_input("ФИО")
    school = st.text_input("Школа")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "История", "Информатика", "Другое"])
    grade = st.selectbox("Класс", [f"{i} класс" for i in range(1, 12)])

topic = st.text_input("Тема урока")

# 5. Логика генерации
if st.button("Сгенерировать"):
    if not topic:
        st.warning("Введите тему!")
    else:
        with st.spinner('Работаю...'):
            try:
                prompt = f"Составь КСП. Учитель: {fio}, Школа: {school}, Предмет: {subject}, Класс: {grade}. Тема: {topic}."
                response = model.generate_content(prompt)
                st.session_state['plan'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ошибка API: {e}")

# 6. Экспорт
if 'plan' in st.session_state:
    doc = Document()
    doc.add_paragraph(st.session_state['plan'])
    bio = io.BytesIO()
    doc.save(bio)
    st.download_button("📥 Скачать в Word", data=bio.getvalue(), file_name="КСП.docx")

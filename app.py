import streamlit as st
import google.generativeai as genai
import io
from docx import Document

st.set_page_config(page_title="Конструктор КСП", layout="wide")

# Проверка ключа
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Ключ не найден в Secrets!")
    st.stop()

# Инициализация
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Интерфейс
fio = st.text_input("ФИО учителя")
topic = st.text_input("Тема урока")

if st.button("Сгенерировать"):
    with st.spinner('Генерирую...'):
        try:
            prompt = f"Составь подробный КСП на тему: {topic}. Учитель: {fio}."
            response = model.generate_content(prompt)
            st.session_state['plan'] = response.text
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Ошибка: {e}")

# Экспорт
if 'plan' in st.session_state:
    doc = Document()
    doc.add_paragraph(st.session_state['plan'])
    bio = io.BytesIO()
    doc.save(bio)
    st.download_button("Скачать в Word", data=bio.getvalue(), file_name="КСП.docx")

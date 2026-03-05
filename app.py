import streamlit as st
import google.generativeai as genai
import io
from docx import Document

# Настройка
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Используем 1.0-pro, она самая стабильная и доступная для всех
model = genai.GenerativeModel('gemini-1.0-pro')

st.title("🎓 Конструктор КСП")
fio = st.text_input("ФИО")
topic = st.text_input("Тема урока")

if st.button("Сгенерировать"):
    try:
        # Простой запрос без лишней логики
        response = model.generate_content(f"Составь план урока на тему: {topic}. Учитель: {fio}")
        st.session_state['plan'] = response.text
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Ошибка API: {e}")

# Экспорт
if 'plan' in st.session_state:
    doc = Document()
    doc.add_paragraph(st.session_state['plan'])
    bio = io.BytesIO()
    doc.save(bio)
    st.download_button("Скачать в Word", data=bio.getvalue(), file_name="plan.docx")

import streamlit as st
import google.generativeai as genai
import io
from docx import Document

st.set_page_config(page_title="Конструктор КСП", layout="wide")
st.title("🎓 Конструктор КСП")

# 1. Загрузка ключа из Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Ключ GOOGLE_API_KEY не найден в Settings -> Secrets.")
    st.stop()

# 2. Настройка модели БЕЗ поиска (исключаем ошибки перебора)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Используем 1.0-pro, так как она самая стабильная для всех ключей
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    st.error(f"Ошибка настройки: {e}")
    st.stop()

# 3. Интерфейс
with st.sidebar:
    st.header("Данные")
    fio = st.text_input("ФИО")
    school = st.text_input("Школа")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "История", "Информатика", "Другое"])
    grade = st.selectbox("Класс", [f"{i} класс" for i in range(1, 12)])

topic = st.text_input("Тема урока")

# 4. Логика генерации
if st.button("Сгенерировать"):
    if not topic:
        st.warning("Введите тему!")
    else:
        with st.spinner('Генерирую...'):
            try:
                # Четкий запрос
                prompt = f"Составь подробный КСП (план урока) по ГОСО. Учитель: {fio}. Школа: {school}. Предмет: {subject}. Класс: {grade}. Тема: {topic}."
                response = model.generate_content(prompt)
                st.session_state['plan'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ошибка API: {e}")
                st.info("Совет: если ошибка 404 сохраняется, создай НОВЫЙ проект в Google AI Studio.")

# 5. Экспорт
if 'plan' in st.session_state:
    doc = Document()
    doc.add_paragraph(st.session_state['plan'])
    bio = io.BytesIO()
    doc.save(bio)
    st.download_button("📥 Скачать в Word", data=bio.getvalue(), file_name="КСП.docx")

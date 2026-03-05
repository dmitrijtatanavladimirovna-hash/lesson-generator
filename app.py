import streamlit as st
import google.generativeai as genai
import io
from docx import Document

st.set_page_config(page_title="Конструктор КСП", layout="wide")
st.title("🎓 Конструктор КСП")

# 1. Настройка ключа
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Ключ GOOGLE_API_KEY не найден. Перейди в Settings -> Secrets.")
    st.stop()

# 2. Настройка модели (жестко задаем имя)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Используем проверенное имя модели
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Ошибка при инициализации модели: {e}")
    st.stop()

# 3. Боковая панель
with st.sidebar:
    st.header("Данные педагога")
    fio = st.text_input("ФИО педагога")
    school = st.text_input("Школа")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "История", "Информатика", "Другое"])
    grade = st.selectbox("Класс", [f"{i} класс" for i in range(1, 12)])

# 4. Основная логика
topic = st.text_input("Тема урока")

if st.button("Сгенерировать план"):
    if not topic:
        st.warning("Введите тему!")
    else:
        with st.spinner('Генерирую...'):
            try:
                prompt = f"Составь подробный КСП для {fio}, школа {school}, {grade}, {subject}. Тема: {topic}. Структура: Цели, Этапы урока (таблица), Оценивание, Рефлексия."
                response = model.generate_content(prompt)
                st.session_state['plan'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ошибка при генерации: {e}")

# 5. Экспорт
if 'plan' in st.session_state:
    doc = Document()
    doc.add_paragraph(st.session_state['plan'])
    bio = io.BytesIO()
    doc.save(bio)
    st.download_button("📥 Скачать в Word", data=bio.getvalue(), file_name="КСП.docx")

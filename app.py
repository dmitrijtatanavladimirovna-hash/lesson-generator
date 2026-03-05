import streamlit as st
import google.generativeai as genai
import io
from docx import Document

# Настройка страницы
st.set_page_config(page_title="Профессиональный Генератор КСП", layout="wide")
st.title("🎓 Профессиональный конструктор КСП")

# Настройка API
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("Ключ API не найден. Проверь настройки Secrets.")
    st.stop()

# --- Боковая панель: Данные учителя ---
with st.sidebar:
    st.header("Данные учителя")
    fio = st.text_input("ФИО педагога")
    school = st.text_input("Название школы")
    subject = st.selectbox("Предмет", ["Математика", "Алгебра", "Геометрия", "Физика", "Химия", "Биология", "История", "География", "Информатика", "Другое"])
    grade = st.selectbox("Класс", [f"{i} класс" for i in range(1, 12)])

# --- Вкладки интерфейса ---
tab1, tab2 = st.tabs(["📋 Ввод данных", "📄 Просмотр и Word"])

with tab1:
    topic = st.text_input("Тема урока")
    col1, col2 = st.columns(2)
    with col1:
        learning_objectives = st.text_area("Цели обучения (из КТП)")
        differentiation = st.selectbox("Тип дифференциации", ["Задания", "Темп", "Поддержка", "Диалог"])
    with col2:
        evaluation = st.text_area("Критерии оценивания")
        reflection = st.text_area("Рефлексия (вопросы)")

    if st.button("Сгенерировать план"):
        if not topic or not learning_objectives:
            st.warning("Заполните тему и цели!")
        else:
            with st.spinner('Генерирую профессиональный план...'):
                prompt = f"""
                Составь КСП (Краткосрочный план) по ГОСО РК.
                Учитель: {fio}, Школа: {school}.
                Предмет: {subject}, Класс: {grade}.
                Тема: {topic}.
                Цели: {learning_objectives}.
                Дифференциация: {differentiation}.
                Оценивание: {evaluation}.
                Рефлексия: {reflection}.

                СТРУКТУРА:
                1. Цели урока (SMART).
                2. Ход урока (Таблица: Этап, Время, Действия, Оценивание).
                3. Ресурсы.
                4. Дифференциация (как именно реализуется).
                5. Рефлексия (вопросы к ученикам).
                """
                response = model.generate_content(prompt)
                st.session_state['plan'] = response.text
                st.success("План готов! Перейдите во вкладку 'Просмотр и Word'.")

with tab2:
    if 'plan' in st.session_state:
        st.markdown(st.session_state['plan'])
        
        # Генерация Word
        doc = Document()
        doc.add_heading('КСП Урока', 0)
        doc.add_paragraph(st.session_state['plan'])
        bio = io.BytesIO()
        doc.save(bio)
        
        st.download_button(
            label="📥 Скачать в Word",
            data=bio.getvalue(),
            file_name=f"{topic}_КСП.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.info("Сначала сгенерируйте план во вкладке 'Ввод данных'")

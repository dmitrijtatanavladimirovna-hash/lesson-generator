import streamlit as st
import google.generativeai as genai

# Настройка страницы
st.set_page_config(page_title="Генератор уроков", page_icon="📝")
st.title("📝 Генератор планов уроков")

# Получаем ключ из Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Ошибка доступа к API-ключу. Проверь настройки Secrets в Streamlit.")
    st.stop()

# Инициализация модели
model = genai.GenerativeModel('gemini-1.5-flash')

# Форма ввода данных
with st.sidebar:
    st.header("Данные учителя")
    fio = st.text_input("ФИО педагога")
    
    st.header("Параметры урока")
    subject = st.selectbox("Выберите предмет", [
        "Математика", "Алгебра", "Геометрия", "Физика", "Химия", "Биология", 
        "История", "География", "Литература", "Русский язык", "Английский язык", 
        "Информатика", "Обществознание", "Другое"
    ])
    
    grade = st.selectbox("Класс", list(range(1, 12)))

# Основная часть
topic = st.text_input("Какая тема урока?")

if st.button("Сгенерировать план"):
    if topic and fio:
        with st.spinner('Пишу план...'):
            try:
                prompt = f"""
                Составь подробный план урока.
                Учитель: {fio}
                Предмет: {subject}
                Класс: {grade}
                Тема: {topic}
                
                Включи в план: цели урока, структуру (этапы), основные понятия, 
                методы проверки знаний и домашнее задание.
                """
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
    else:
        st.warning("Пожалуйста, заполни ФИО и тему урока.")

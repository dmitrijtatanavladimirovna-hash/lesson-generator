import streamlit as st
import google.generativeai as genai
import io
from docx import Document

# 1. Настройка страницы
st.set_page_config(page_title="Генератор КСП", layout="wide")
st.title("🎓 Конструктор КСП (Краткосрочный план)")

# 2. Подключение API
# Важно: Streamlit ищет GOOGLE_API_KEY в настройках Secrets (Settings -> Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Ошибка: Ключ GOOGLE_API_KEY не найден в настройках Secrets.")
    st.stop()

# 3. Инициализация модели (используем самую стабильную версию)
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Ошибка при подключении к модели: {e}")
    st.stop()

# 4. Интерфейс
with st.sidebar:
    st.header("Данные педагога")
    fio = st.text_input("ФИО педагога")
    school = st.text_input("Школа")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "Химия", "Биология", "История", "Информатика", "Другое"])
    grade = st.selectbox("Класс", [f"{i} класс" for i in range(1, 12)])

tab1, tab2 = st.tabs(["📋 Ввод данных", "📄 Результат"])

with tab1:
    topic = st.text_input("Тема урока")
    col1, col2 = st.columns(2)
    with col1:
        objectives = st.text_area("Цели обучения")
    with col2:
        evaluation = st.text_area("Критерии оценивания")

    if st.button("Сгенерировать план"):
        if not topic:
            st.warning("Введите тему урока!")
        else:
            with st.spinner('Генерирую...'):
                try:
                    prompt = f"""
                    Составь подробный КСП по теме: {topic}.
                    Учитель: {fio}, Школа: {school}.
                    Предмет: {subject}, Класс: {grade}.
                    Цели: {objectives}.
                    Критерии: {evaluation}.
                    
                    Выдай результат в виде четкого плана с таблицей этапов урока.
                    """
                    response = model.generate_content(prompt)
                    st.session_state['plan'] = response.text
                    st.success("План готов!")
                except Exception as e:
                    st.error(f"Ошибка генерации: {e}")

with tab2:
    if 'plan' in st.session_state:
        st.markdown(st.session_state['plan'])
        
        # Генерация Word
        doc = Document()
        doc.add_heading('КСП', 0)
        doc.add_paragraph(st.session_state['plan'])
        bio = io.BytesIO()
        doc.save(bio)
        
        st.download_button("📥 Скачать в Word", data=bio.getvalue(), file_name="КСП.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    else:
        st.info("Сначала сгенерируйте план во вкладке 'Ввод данных'")

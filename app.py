import streamlit as st
import google.generativeai as genai
import io
from docx import Document

st.set_page_config(page_title="Конструктор КСП", layout="wide")
st.title("🎓 Конструктор КСП")

# 1. Настройка
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Ключ не найден в Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. АВТОМАТИЧЕСКИЙ ПОИСК МОДЕЛИ (решает проблему 404)
@st.cache_resource
def get_model():
    # Получаем список всех моделей, которые поддерживают генерацию контента
    models = [m for m in genai.list_models() if 'generateContent' in m.supported_methods]
    if not models:
        return None
    # Берем первую доступную модель (например, gemini-pro или flash, какая есть)
    return genai.GenerativeModel(models[0].name)

model = get_model()

if model is None:
    st.error("Google не вернул ни одной доступной модели. Проверьте ваш API-ключ.")
    st.stop()

# 3. Интерфейс (Боковая панель)
with st.sidebar:
    st.header("Данные")
    fio = st.text_input("ФИО")
    school = st.text_input("Школа")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "История", "Информатика", "Другое"])
    grade = st.selectbox("Класс", [f"{i} класс" for i in range(1, 12)])

# 4. Основная логика
topic = st.text_input("Тема урока")

if st.button("Сгенерировать план"):
    if not topic:
        st.warning("Введите тему!")
    else:
        with st.spinner(f'Работаю через модель: {model.model_name}...'):
            try:
                prompt = f"Составь КСП для {fio}, школа {school}, {grade}, {subject}. Тема: {topic}. Структура: Цели, Этапы (таблица), Оценивание, Рефлексия."
                response = model.generate_content(prompt)
                st.session_state['plan'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ошибка: {e}")

# 5. Экспорт
if 'plan' in st.session_state:
    doc = Document()
    doc.add_paragraph(st.session_state['plan'])
    bio = io.BytesIO()
    doc.save(bio)
    st.download_button("📥 Скачать в Word", data=bio.getvalue(), file_name="КСП.docx")

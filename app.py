import streamlit as st
import google.generativeai as genai

st.title("🎓 Генератор КСП")

# 1. Проверка ключа
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Ошибка: Добавьте GOOGLE_API_KEY в Secrets (Settings -> Secrets)")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. АВТОМАТИЧЕСКИЙ ПОИСК МОДЕЛИ (решает проблему 404)
@st.cache_resource
def get_available_model():
    # Запрашиваем у Google список всех разрешенных нам моделей
    models = [m for m in genai.list_models() if 'generateContent' in m.supported_methods]
    if not models:
        return None
    # Берем первую доступную
    return genai.GenerativeModel(models[0].name)

model = get_available_model()

if model is None:
    st.error("Google не вернул ни одной доступной модели. Проверьте ваш API-ключ.")
    st.stop()

# 3. Интерфейс
topic = st.text_input("Тема урока")

if st.button("Сгенерировать"):
    if topic:
        with st.spinner(f'Генерирую через модель {model.model_name}...'):
            try:
                response = model.generate_content(f"Составь план урока на тему: {topic}")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ошибка: {e}")

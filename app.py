import streamlit as st
import google.generativeai as genai
import io
from docx import Document

# Настройка API (используем секреты, чтобы не "светить" ключ в коде)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Ошибка API ключа: убедись, что ключ добавлен в настройки приложения (Secrets).")
    st.stop()

st.set_page_config(page_title="Генератор КСП", layout="wide")
st.title("🎓 Конструктор планов уроков (ГОСО РК)")

# Функция генерации Word
def create_word_doc(content):
    doc = Document()
    doc.add_heading('Краткосрочный план урока', 0)
    for line in content.split('\n'):
        line = line.strip()
        if line:
            if line.startswith("#"):
                doc.add_heading(line.replace("#", "").strip(), level=1)
            else:
                doc.add_paragraph(line)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# Боковая панель
with st.sidebar:
    st.header("Ввод данных")
    subject = st.text_input("Предмет", value="Физика")
    grade = st.selectbox("Класс", ["7 класс", "8 класс", "9 класс", "10 класс (ЕМН)", "11 класс"])
    topic = st.text_input("Тема урока")
    objectives = st.text_area("Цели обучения (скопируй из КТП)")
    values = st.multiselect("Ценности АДАЛ АЗАМАТ", 
                            ["Ответственность", "Честность", "Научная добросовестность", "Патриотизм"])

# Логика
if st.button("Сгенерировать КСП"):
    if not topic or not objectives:
        st.warning("Заполни тему и цели!")
    else:
        prompt = f"""
        Ты — методист по физике. Составь профессиональный КСП по теме: {topic} для {grade}.
        Цели обучения: {objectives}.
        Прививаемые ценности: {', '.join(values)}.
        
        СТРУКТУРА ПЛАНА:
        1. Раздел программы (подбери по теме).
        2. Цели урока (SMART).
        3. Ход урока (таблица: Этап | Время | Действия педагога | Действия учащихся).
        4. Дифференциация и Оценивание.
        5. Рефлексия.
        
        Используй официально-деловой стиль ГОСО РК. Пиши четко, без лишней "воды".
        """
        
        with st.spinner("Создаю план..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.session_state['generated_plan'] = response.text
            st.markdown(response.text)

# Кнопка скачивания
if 'generated_plan' in st.session_state:
    st.divider()
    docx_data = create_word_doc(st.session_state['generated_plan'])
    st.download_button(
        label="📥 Скачать в Word (.docx)",
        data=docx_data,
        file_name="Plan_uroka.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
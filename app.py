import streamlit as st
from openai import OpenAI
import io
from docx import Document

# Настройка страницы
st.set_page_config(page_title="Конструктор КСП (GPT)", layout="wide")
st.title("🎓 Конструктор КСП (на базе GPT-4o)")

# Подключение к OpenAI
# Важно: В Streamlit Secrets теперь нужен ключ с именем OPENAI_API_KEY
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("❌ Ключ OPENAI_API_KEY не найден в настройках Secrets!")
    st.stop()

# Интерфейс
fio = st.sidebar.text_input("ФИО педагога")
topic = st.text_input("Тема урока")

if st.button("Сгенерировать план"):
    if not topic:
        st.warning("Введите тему урока!")
    else:
        with st.spinner('GPT пишет план...'):
            try:
                # Запрос к OpenAI
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Ты профессиональный методист. Составь подробный КСП (Краткосрочный план) по ГОСО."},
                        {"role": "user", "content": f"Учитель: {fio}. Тема: {topic}. Составь план с таблицей этапов."}
                    ]
                )
                
                plan_text = response.choices[0].message.content
                st.session_state['plan'] = plan_text
                st.markdown(plan_text)
                
            except Exception as e:
                st.error(f"Ошибка API OpenAI: {e}")

# Выгрузка в Word
if 'plan' in st.session_state:
    doc = Document()
    doc.add_paragraph(st.session_state['plan'])
    bio = io.BytesIO()
    doc.save(bio)
    st.download_button("📥 Скачать в Word", data=bio.getvalue(), file_name="КСП.docx")

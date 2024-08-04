#streamlit run app.py --server.fileWatcherType none
import streamlit as st
import pandas as pd
from agent import BookFilterAgent,BookSearchAgent,CoordinatorAgent


book_search_agent = BookSearchAgent()
book_filter_agent = BookFilterAgent()
coordinator_agent = CoordinatorAgent(book_search_agent, book_filter_agent)


def display_books(books):
    for book in books:
        title = book.get('volumeInfo', {}).get('title', 'Başlık bulunamadı')
        authors = book.get('volumeInfo', {}).get('authors', ['Yazar bulunamadı'])
        st.write(f"**Başlık**: {title}")
        st.write(f"**Yazar**: {', '.join(authors)}")
        st.write('-' * 40)


st.title("Google Books API-Agents Example")

image_url = 'data:image/png;base64,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'
st.image(image_url, caption='', use_column_width=True)

user_input = st.text_input(" ")

button1 = st.button("Search")
if button1:
    st.title("Results")
    books = coordinator_agent.find_and_filter_books(user_input)
    display_books(books)
    # st.markdown(
    #     f"""
    #     <style>
    #     .dataframe {{ width: 80%; }}
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )






# text = speech_to_text(
#     language='tr',
#     start_prompt="Start recording",
#     stop_prompt="Stop recording",
#     just_once=False,
#     use_container_width=False,
#     callback=None,
#     args=(),
#     kwargs={},
#     key=None
# )



# st.write(text)


# def callback():
#     if st.session_state.my_stt_output:
#         st.write(st.session_state.my_stt_output)


# r = speech_to_text(key='my_stt', callback=callback)
#st.write(r)

# button1 = st.button("Click Me")
# if button1:
#     text = load_text("xx.txt")
#     st.write(text)

# uploaded_file = st.file_uploader("Bir dosya seçin", type=['txt'])
# if uploaded_file is not None:
#     # # Dosya bilgilerini göster
#     # st.write("Dosya Adı: ", uploaded_file.name)
#     # st.write("Dosya Tipi: ", uploaded_file.type)
#     # st.write("Dosya Boyutu: ", uploaded_file.size, "bytes")

#     if uploaded_file.type == "text/plain":
#         content = uploaded_file.read().decode("utf-8")
#         #st.text_area(" ",content, height=300)


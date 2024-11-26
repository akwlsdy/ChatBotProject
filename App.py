import streamlit as st
from langchain_ollama import ChatOllama  # Updated import to use the new library
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate

class ChatWeb:
    def __init__(self, page_title="Gazzi Chatbot", page_icon=":books:"):
        self._page_title = page_title
        self._page_icon = page_icon
        self._llm = ChatOllama(model="gemma2:2b", temperature=3)  # Make sure the model and parameters are correct

    def setup_ui(self):
        st.set_page_config(page_title=self._page_title, page_icon=self._page_icon)
        st.title(self._page_title)
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

    def process_input(self):
        user_input = st.chat_input("Please enter your question:")
        if user_input:
            st.chat_message("user").write(f"{user_input}")
            st.session_state["messages"].append(user_input)
            return user_input
        return None

    def generate_response(self, user_input):
        if user_input:
            try:
                response = self._llm.invoke(user_input)
                with st.chat_message("assistant"):
                    st.write(response)
                st.session_state["messages"].append(response)
            except ConnectionError as e:
                st.error(f"Failed to connect to the model backend: {str(e)}")
                # You might want to log this error or take further action.

    def run(self):
        self.setup_ui()
        user_input = self.process_input()
        self.generate_response(user_input)

if __name__ == '__main__':
    chat_web = ChatWeb()
    chat_web.run()

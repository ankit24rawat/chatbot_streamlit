import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

# Page Config (adds a title to the browser tab)
st.set_page_config(page_title="AI Assistant", page_icon="🤖")

# 1. Initialize session state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# 2. UI Logic: Show Welcome Screen OR Chat History
if not st.session_state['message_history']:
    # --- WELCOME SCREEN (Shown when history is empty) ---
    st.write("##") # Add some spacing
    st.title("Welcome to My AI Assistant! 👋")
    
    # You can use a URL for an image or a local file path
    st.image("https://ui-avatars.com/api/?name=AI&background=random&size=128", width=100)
    
    st.markdown("""
    I am powered by **LangGraph** and **OpenAI**.  
    How can I help you today? Try asking:
    * *'What is the weather in Paris?'*
    * *'Explain quantum physics like I'm five.'*
    """)
    # ----------------------------------------------------
else:
    # --- CHAT INTERFACE (Shown when there are messages) ---
    for message in st.session_state['message_history']:
        with st.chat_message(message['role']):
            # st.markdown looks much better than st.text for AI responses
            st.markdown(message['content'])

# 3. Chat Input
user_input = st.chat_input('Type here...')

if user_input:
    # Display the user message immediately
    with st.chat_message('user'):
        st.markdown(user_input)
    
    # Add to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

    # Generate AI response
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config={'configurable': {'thread_id': 'thread-1'}},
                stream_mode='messages'
            )
        )

    # Add AI response to history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    
    # Force a rerun to clean up the UI and hide the welcome screen immediately
    st.rerun()
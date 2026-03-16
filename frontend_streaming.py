import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# Set Page Config at the very top
st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖", layout="wide")

# **************************************** utility functions *************************

def generate_thread_id():
    return str(uuid.uuid4()) # Convert to string for easier button handling

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])


# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])


# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('➕ New Chat', use_container_width=True):
    reset_chat()
    st.rerun() # Refresh to show welcome screen

st.sidebar.divider()
st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    # Display a shortened version of the UUID for the button label
    label = f"Chat {thread_id[:8]}..."
    if st.sidebar.button(label, key=thread_id, use_container_width=True):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []
        for msg in messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages
        st.rerun()


# **************************************** Main UI ************************************

# 1. THE FIX: Check if message history is empty
if not st.session_state['message_history']:
    st.write("##") # Spacing
    st.title("Welcome to your AI Workspace! 🚀")
    
    # Placeholder Image (Replace URL with your own if desired)
    st.image("robot.png", width=100)
    
    st.markdown("""
    ### How to get started:
    1. **Type a message** in the box below to start a new thread.
    2. **View history** in the sidebar to return to previous chats.
    3. **Click "New Chat"** to reset the current view.
    
    I can help you write code, answer questions, or just chat!
    """)
else:
    # 2. Loading the conversation history (Updated to st.markdown)
    for message in st.session_state['message_history']:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# 3. Chat Input
user_input = st.chat_input('Type here')

if user_input:
    # Add user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    
    with st.chat_message('user'):
        st.markdown(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message("assistant"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

    # Save to history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    
    # 4. Rerun to ensure UI stays consistent (hides welcome screen if this was the first message)
    st.rerun()
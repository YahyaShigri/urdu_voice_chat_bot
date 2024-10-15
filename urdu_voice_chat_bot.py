from langchain.prompts import (
    ChatPromptTemplate,  # AI se prompts generate karne ke liye template
    HumanMessagePromptTemplate,  # Human user ke input ka template
    MessagesPlaceholder,  # Messages ke liye placeholder jo history handle karta hai
    SystemMessagePromptTemplate,  # System messages ka template jo AI ko instructions deta hai
)
from langchain_community.chat_message_histories import StreamlitChatMessageHistory  # Chat history ko store karne ke liye
from langchain_core.runnables.history import RunnableWithMessageHistory  # Model ko chat history k sath run karne ke liye
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Generative AI ko integrate karta hai
from langchain.schema.output_parser import StrOutputParser  # AI response ko string format main parse karta hai
from streamlit_mic_recorder import speech_to_text  # Voice input ko text main convert karta hai
from gtts import gTTS  # Text ko speech main convert karne ke liye
from gtts.lang import tts_langs  # Available languages ke list
import streamlit as st  # Streamlit ko import kiya gaya hai jo UI banata hai
import os  # OS related functions ke liye
from dotenv import load_dotenv  # For loading environment variables

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")  # Get the Google API key from the .env file

# Streamlit app ka page configuration set karta hai
st.set_page_config(page_title="AI Voice Assistant", page_icon="🤖")

# App ka title aur subtitle show karta hai
st.title("AI Voice Assistant 🎙️")
st.subheader("Interact in Urdu with Real-Time Voice Input")
# App main aik image display karta hai
st.image("https://cdn.prod.website-files.com/647049f40d72f61b1a42f2c3/655c5376c61409993c6f177b_799451f7-9354-438b-a36e-67d9b8530f1f.webp", use_column_width=True)
# Prompt template jo AI ko input deta hai aur chat history ko track karta hai
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a helpful AI assistant. Please always respond to user queries in Pure Urdu language."  # AI ko Urdu main jawab dene ka instruction deta hai
        ),
        MessagesPlaceholder(variable_name="chat_history"),  # Chat history ko track karta hai
        HumanMessagePromptTemplate.from_template("{question}"),  # Human user ke sawal ka template
    ]
)

# Streamlit chat message history ko store karne ke liye
msgs = StreamlitChatMessageHistory(key="langchain_messages")

# Google Generative AI model ko load karta hai
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# Chain setup jo AI se response le kar output ko parse karta hai
chain = prompt | model | StrOutputParser()

# Chain ko history k sath run karta hai taake AI pichlay messages ko bhi samjh sakay
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,  # Session ID ke sath messages ko link karta hai
    input_messages_key="question",  # Input main user ka question pass karta hai
    history_messages_key="chat_history",  # History main purani chat pass karta hai
)

# Available languages ko check karta hai jo TTS support karta hai
langs = tts_langs().keys()

# Function to check if the query is related to app creator information
def is_app_related_query(query):
    keywords = [
        "create", "develop", "make", "creator", "who", "author", "about you", 
        "built", "designed", "constructed", "programmed", 
        "engineered", "invented", "origin", "authored", 
        "who made", "who created", "who built", "who designed", 
        "who constructed", "who invented",
        # Urdu keywords
        "آپ", "کون", "بنایا", "تخلیق", "خالق", "مصنف", "ڈیزائنر", "کس نے"
    ]
    # Convert query to lowercase and check for keywords
    return any(keyword in query.lower() for keyword in keywords)

# UI pe instruction deta hai ke mic button dabao aur Urdu main bolna shuru karo
st.write("Press the button and start speaking in Urdu:")

# Spinner show karta hai jab tak speech to text conversion chal raha hota hai
with st.spinner("Converting Speech To Text..."):
    # Speech ko Urdu main text main convert karta hai
    text = speech_to_text(
        language="ur", use_container_width=True, just_once=True, key="STT"
    )

# Agar speech successfully text main convert ho jaye
if text:
    # Human message ko chat main display karta hai
    st.chat_message("human").write(text)
    
    # Check if the query is about the app's creator
    if is_app_related_query(text):
        creator_response = "I was created by Yahya Khan Shigri. You can find him at www.linkedin.com/in/yahya-khan-shigri."
        st.chat_message("assistant").write(creator_response)

        # Convert the response to speech
        with st.spinner("Converting Text To Speech..."):
            tts = gTTS(text=creator_response, lang="ur")
            tts.save("output.mp3")
            st.audio("output.mp3")
    else:
        # AI ka response chat main dikhata hai
        with st.chat_message("assistant"):
            message_placeholder = st.empty()  # Empty placeholder for AI response
            full_response = ""  # AI ka full response yahan save hota hai

            # Session ke config settings
            config = {"configurable": {"session_id": "any"}}
            # AI model se response stream karta hai aur response ko show karta hai
            response = chain_with_history.stream({"question": text}, config)

            # AI ka response step by step show karta hai
            for res in response:
                full_response += res or ""
                message_placeholder.markdown(full_response + "|")  # Live updating response
                message_placeholder.markdown(full_response)  # Final response display

        # Spinner show karta hai jab tak text to speech conversion chal raha hota hai
        with st.spinner("Converting Text To Speech..."):
            # AI ke jawab ko Urdu speech main convert karta hai
            tts = gTTS(text=full_response, lang="ur")
            # Speech ko save karta hai
            tts.save("output.mp3")
            # Output ko play karta hai
            st.audio("output.mp3")

# Agar user ne speech record nahi ki
else:
    # Warning message show karta hai
    st.warning("Please press the button and start speaking.")

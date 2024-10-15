AI Voice Assistant 🎙️
This project is an AI Voice Assistant that allows users to interact in real-time using voice input in Urdu. The assistant processes speech input, converts it into text, interacts with an AI model, and provides responses in Urdu. The assistant can also convert the AI's response back into speech for a complete conversational experience.

Features
Voice Input: The app captures speech input in Urdu and converts it to text.
Urdu Responses: The AI assistant responds to queries in Urdu.
Text-to-Speech (TTS): Converts the AI's responses from text back to speech in Urdu, enabling a full conversational flow.
Streamed Responses: Real-time, streamed responses from the AI as the conversation unfolds.
Chat History: Keeps track of the conversation history to maintain context across interactions.
Technology Stack
LangChain: Manages prompts, chat history, and chain functionality.
Google Generative AI: Leverages Google Generative AI (Gemini 1.5 Flash) for intelligent responses.
Streamlit: Provides the interactive UI for the web application.
Google Text-to-Speech (gTTS): Converts text into Urdu speech.
Streamlit Mic Recorder: Captures voice input and converts it into text using speech-to-text.
Installation
Follow these steps to set up the project:

Clone the repository:

bash
Copy code
git clone https://github.com/your-username/urdu-voice-assistant.git
cd urdu-voice-assistant
Create a virtual environment:

bash
Copy code
conda create -n urdu_voice_chatbot python=3.9
conda activate urdu_voice_chatbot
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the app:

bash
Copy code
streamlit run app.py
Dependencies
The project requires the following libraries, listed in requirements.txt:

langchain
langchain-community
langchain-google-genai
streamlit-mic-recorder
gtts
streamlit
Usage
Press the microphone button on the app.
Start speaking in Urdu.
The app will convert your speech into text, send it to the AI, and display the AI's response.
The AI's response will also be spoken aloud in Urdu.
Acknowledgments
This project would not have been possible without the support and contributions of the following individuals:

Sir Irfan Malik
Dr. Sheraz
Sir Haris
I also want to express my sincere thanks to Bushra Akram for her invaluable content, which greatly assisted in the development of this project. Check out her YouTube channel for amazing tutorials: Bushra Akram""https://www.youtube.com/@Bushra_Akram_/featured"".


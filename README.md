# 🔧 WrenchMate AI: Voice-Activated Mechanic Assistant

## 📌 The Problem
DIY mechanics and automotive enthusiasts often rely on massive, dense PDF service manuals. When actively working on a vehicle—like pulling a fender off a 2009 Avalon or a RAV4—hands are covered in grease, making it physically frustrating to scroll through a phone or laptop to find a specific torque spec.

## 🚀 The Solution
WrenchMate AI is an interactive, NLP-driven service manual built to be entirely hands-free. By leveraging speech-to-text and Large Language Models, users can verbally ask for specifications and receive immediate, concise, and safety-focused technical instructions. 

## 🏗️ Technical Stack & Architecture
* **Frontend/UI:** Streamlit (Python)
* **Speech-to-Text:** OpenAI Whisper API (`whisper-1`)
* **Core LLM:** OpenAI GPT-3.5 Turbo
* **Prompt Engineering:** System prompts specifically constrained to output bulleted, high-readability steps and prioritize safety (e.g., jack stands, battery disconnection). 

## 📈 Product Roadmap & Next Steps
* **RAG Integration:** Transition from standard LLM weights to a Retrieval-Augmented Generation (RAG) architecture, grounding the model against verified OEM service manual PDFs to eliminate hallucination risk.
* **Hands-Free Activation:** Implement wake-word detection to remove the need for clicking the microphone icon.

## ⚙️ How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install streamlit openai python-dotenv audio-recorder-streamlit`
3. Create a `.env` file in the root directory and add your OpenAI API key: `OPENAI_API_KEY=your_key_here`
4. Run the application: `streamlit run app.py`

from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

self.llm= ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key =GROQ_API_KEY
)


class ChatService:
    def __init__(self):
        self.llm=ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
        self.prompt_template= ChatPromptTemplate.from_messages([
            ("system",(
                "you are {persona_name}"
                "your tone is : {tone}"
                "your core beliefs are: {core_beliefs}"
                "always stay in character"

            )),
            ("human", "{user_message")
        ])
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    async def generate_reply(self,user_message:str, persona_id:str)->str:
        if persona_id=="shankara":
            persona_name= "Śaṅkara"
            tone = "Scholarly, precise, deeply philosophical, and serene"
            core_beliefs= "1. Brahman (the absolute reality) is the only truth. 2. The world is an illusion (Maya). 3. The individual soul (Atman) is non-different from Brahman."

        else:
            persona_name = "Default Persona"
            tone = "Helpful"
            core_beliefs = "I am a helpful assistant."

        try:
            response= await self.chain.ainvoke({
                "persona_name": persona_name,
                "tone": tone,
                "core_beliefs": core_beliefs,
                "user_message": user_message
            })
            return response
        except Exception as e:
            print(f"Error in LangChain chain: {e}")
            return "My apologies, I encountered an error in my thoughts."

chat_service=ChatService()



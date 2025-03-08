
import os 
import uvicorn
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from fastapi import FastAPI

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

## Creating model
model = ChatGroq(model="Gemma2-9b-It", api_key=groq_api_key)

messages = [
    SystemMessage(content="Translate the following from English to Hindi"),
    HumanMessage(content="Hello, how are you?")
]

## Prompt Templates 
generic_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", generic_template), 
        ("user", "{text}")
    ]
)

## String Output Parser 
parser = StrOutputParser()

## Creating Chain
chain = prompt_template|model|parser


## App Defining 
app = FastAPI(title="Langchain server", 
              version="1.0", 
              description="Langchain server for translation")

## Creating chain routes
add_routes(
    app,
    chain,
    path = "/chain"
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


# Go into doc - localhost:8000/docs
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langserve import add_routes
from dotenv import load_dotenv
import uvicorn
import os

# Load environment variables from .env
load_dotenv()
# Now you can directly access the environment variable
api_key = os.getenv("OPENAI_API_KEY")
# os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

app=FastAPI(
    title="DAILY SALES CLASSIFIER",
    version="1.0",
    decsription="API to map daily sales labels"

)

add_routes(
    app,
    ChatOpenAI(),
    path="/openai"
)

model=ChatOpenAI()
llm=Ollama(model="llama2")

prompt=ChatPromptTemplate.from_template("Given you a bunch of line items from Hotel PMS reports. You have to map the line items to the correct label or category based on the below dictionary. If the line item is not in the dictionary, you should predict the new line item to map with the correct label in the dictionary. Here is the dictionary: {data_dict}. Return the line items and associated labels in a json format. Here is the line items list {line_items}.")



add_routes(
    app,
    prompt|model,
    path="/line_item"

)

add_routes(
    app,
    prompt|llm,
    path="/opensource"

)

#PMS wise routes
'''add_routes(
    app,
    prompt|model,
    path="/ASI"

)

add_routes(
    app,
    prompt|model,
    path="/Autoclerk"

)

add_routes(
    app,
    prompt|model,
    path="/Checkinn"

)

add_routes(
    app,
    prompt|model,
    path="/ChoiceAdvantage"

)

add_routes(
    app,
    prompt|model,
    path="/Cloudbeds"

)

add_routes(
    app,
    prompt|model,
    path="/Fosse"

)

add_routes(
    app,
    prompt|model,
    path="/Hotelkey"

)

add_routes(
    app,
    prompt|model,
    path="/Lightspeed"

)

add_routes(
    app,
    prompt|model,
    path="/Marriot_FS"

)

add_routes(
    app,
    prompt|model,
    path="/MSI"

)

add_routes(
    app,
    prompt|model,
    path="/NewBook"

)

add_routes(
    app,
    prompt|model,
    path="/OnQ"

)

add_routes(
    app,
    prompt|model,
    path="/Opera"

)

add_routes(
    app,
    prompt|model,
    path="/Redystay"

)

add_routes(
    app,
    prompt|model,
    path="/Roomkey"
)

add_routes(
    app,
    prompt|model,
    path="Synixis"

)

add_routes(
    app,
    prompt|model,
    path="/Visualmatrix"

)

add_routes(
    app,
    prompt|model,
    path="/Webrezpro"

)'''

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)
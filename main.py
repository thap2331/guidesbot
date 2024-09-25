from fastapi import FastAPI
import psycopg2, os

app = FastAPI()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_csv import PACrimeBot

app = FastAPI()
pacrimebot = PACrimeBot()
PG_CONNECTION_STRING = os.environ.get("PG_CONNECTION_STRING")

async def add_query_data(data):
    try:
        with psycopg2.connect(PG_CONNECTION_STRING) as conn:
            query = """INSERT INTO query_data (question) VALUES (%s)"""
            with conn.cursor() as cur:
                cur.execute(query, (data,))
                conn.commit()

    except Exception as e:
        print("Error:", e)

    return

class Question(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ask/")
async def create_item(user_data: Question):
    user_question = user_data.question
    await add_query_data(user_question)
    bot_response = pacrimebot.conversational_chat(user_question)
    response = {"response": bot_response}

    return response

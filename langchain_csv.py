import os
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import psycopg2

class PACrimeBot:

    def __init__(self) -> None:
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>")
        self.PG_CONNECTION_STRING=os.environ.get("PG_CONNECTION_STRING")
        self.COLLECTION_NAME = "pa_courts"
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.OPENAI_API_KEY)
        self.store = PGVector(
            collection_name=self.COLLECTION_NAME,
            connection_string=self.PG_CONNECTION_STRING,
            embedding_function=self.embeddings,
        )
        self.create_required_db_tables()

    def bot_qa(self, query):
        response = self.conversational_chat(query)

        return response

    def conversational_chat(self, query):
        chain = ConversationalRetrievalChain.from_llm(
                        llm = ChatOpenAI(temperature=0.0,
                                        model_name='gpt-3.5-turbo', 
                                        openai_api_key=self.OPENAI_API_KEY),
                        retriever=self.store.as_retriever())
        result = chain.invoke({"question": query,
                        "chat_history": []})

        return result["answer"]
    
    def create_required_db_tables(self):
        try:
            with psycopg2.connect(self.PG_CONNECTION_STRING) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS query_data (
                            question_id SERIAL PRIMARY KEY,
                            user_id VARCHAR(50),
                            question VARCHAR(1000)
                        )
                        """
                    )
                    conn.commit()

        except Exception as e:
            print("Error:", e)

        # finally:
        #     # Close communication with the PostgreSQL database
        #     cur.close()
        #     conn.close()
        return

question = "Are there any sexual assault charges filed in the month of February?"
question = "What charges Coady Allen is charged with?"
question = "Tell me about what Mason Edward is charged with and when?"
# question = "Tell me about what Dakota Scott is charged with and when?"
# question = "Give me a list of all sexual assults in February 2024?"
# question = "Give me sexual assult charged in February 2024?"

# pacrimebot = PACrimeBot()
# response = pacrimebot.conversational_chat(question)
# print(response)
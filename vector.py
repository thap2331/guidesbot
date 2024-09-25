import os, psycopg2, argparse
from langchain_community.vectorstores.pgvector import PGVector
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--droptable', '-d', action='store_true', help='Delete this table.')
parser.add_argument('--runmode', '-r', default='dev', choices=["dev", "prod"], help='Delete this table.')

args = parser.parse_args()
RUNMODE = args.runmode
print(f"Running in {RUNMODE} mode")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>")
PG_CONNECTION_STRING=os.environ.get("PG_CONNECTION_STRING")

file_path = "data/results-3900-datapoints.csv"

loader = CSVLoader(file_path=file_path, encoding="utf-8", csv_args={
                'delimiter': ','})
data = loader.load()
if RUNMODE=='dev':
    data = data[0:10] #Limit here for testing as it does costs us money if we use OpenAI


vector_extension_query = """CREATE EXTENSION IF NOT EXISTS vector;"""
conn = psycopg2.connect(PG_CONNECTION_STRING)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

COLLECTION_NAME = "pa_courts"

if args.droptable:
    print(f"Deleting {COLLECTION_NAME} table before readding this table.")
    db = PGVector.from_documents(
        documents= data,
        embedding = embeddings,
        collection_name= COLLECTION_NAME,
        connection_string=PG_CONNECTION_STRING,
        pre_delete_collection=True
        )
else:
    db = PGVector.from_documents(
        documents= data,
        embedding = embeddings,
        collection_name= COLLECTION_NAME,
        connection_string=PG_CONNECTION_STRING
        )
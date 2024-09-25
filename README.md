# pa-legal-bot

## How to get started locally?
- In terms of technology, all you need is docker and makefile.
- Copy `.env-example` to `.env` file. 
    - Add OpenAI key in your .env fole. (For now we are gonna use openAI, but we will eventually replace that with a no-cost option.)
    - Keep the PG_CONNECTION_STRING as it is.

## How to run a bot locally?
- Get your data ready by doing `make gen-embeddings`
- Get into shell of local bot container `make local-bot-shell`
    - Here you can run python commands `python langchain-csv.py`. You can edit questions in `langchain-csv.py`

## How to view your vector data locally?
- Run `make pgweb`

## API test
- `curl -H 'Content-Type: application/json' -d '{"question":"Tell me about what Mason Edward is charged with and when?"}' -X POST http://0.0.0.0:8000/ask/`

## Todo
- should we add a frontend here
- Cite the data coming from
- Add chat history capabiltity
- How good is the bot?
- Remove data folder from github and add this folder to .gitignore
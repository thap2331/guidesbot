local-bot:
	docker compose up --build pacrimebot-local -d

gen-embeddings: local-bot
	docker exec -t pacrimebots-local bash -c "python vector.py"

local-bot-shell:
	docker exec -it pacrimebots-local bash

pgweb:
	docker compose up --build pgweb -d
	open http://localhost:8002
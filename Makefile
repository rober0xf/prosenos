.PHONY: run dev

run:
	uv run fastapi run app/main.py --host 127.0.0.1 --port 8000

dev:
	uv run fastapi run app/main.py --host 127.0.0.1 --port 8000 --reload

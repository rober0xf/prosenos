.PHONY: run dev

run:
	uv run fastapi run app/main.py --host 0.0.0.0 --port 8000

dev:
	uv run fastapi run app/main.py --host 0.0.0.0 --port 8000 --reload

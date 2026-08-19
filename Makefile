.PHONY: run dev

run:
	uv run --no-sync fastapi run app/main.py --host 0.0.0.0 --port 8000

dev:
	uv run --no-sync fastapi run app/main.py --host 0.0.0.0 --port 8000 --reload

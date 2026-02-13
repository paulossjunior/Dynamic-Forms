.PHONY: install backend frontend dev clean

install:
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

backend:
	cd backend && . venv/bin/activate && uvicorn main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

dev:
	@echo "Starting both applications..."
	@(trap 'kill 0' SIGINT; make backend & make frontend)

clean:
	rm -rf backend/venv
	rm -rf frontend/node_modules

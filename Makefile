.PHONY: install backend frontend dev clean stop

install:
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

backend:
	cd backend && . venv/bin/activate && uvicorn main:app --reload --port 8001

frontend:
	cd frontend && npm run dev

dev: stop
	@echo "Starting both applications..."
	@(trap 'kill 0' SIGINT; make backend & make frontend)

clean:
	rm -rf backend/venv
	rm -rf frontend/node_modules

stop:
	@echo "Stopping applications on ports 8001 and 5173..."
	@-lsof -ti :8001 | xargs kill -9 2>/dev/null || true
	@-lsof -ti :5173 | xargs kill -9 2>/dev/null || true
	@echo "Applications stopped."

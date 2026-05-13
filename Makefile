.PHONY: help proto

help:
	@echo "Targets disponibles:"
	@echo "  make dev      - iniciar servidor en modo desarrollo"
	@echo "  make proto    - generar clases Python desde .proto"


proto:
	@if [ "$(SHELL)" = "/bin/fish" ]; then \
		fish ./scripts/generate_proto.fish; \
	else \
		./scripts/generate_proto.sh; \
	fi

dev:
	@if [ "$(SHELL)" = "/bin/fish" ]; then \
		source strategy/.venv/bin/activate.fish; \
	else \
		source strategy/.venv/bin/activate; \
	fi && uvicorn strategy.src.server.main:app --reload
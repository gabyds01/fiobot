.PHONY: help proto

help:
	@echo "Targets disponibles:"
	@echo "  make proto    - generar clases Python desde .proto"


proto:
	@if [ "$(SHELL)" = "/bin/fish" ]; then \
		fish ./scripts/generate_proto.fish; \
	else \
		./scripts/generate_proto.sh; \
	fi
.PHONY: help validate validate-strict validate-deep audit-substrate install-hook uninstall-hook

# Default target
help:
	@echo "PhantomOS workspace · commandes disponibles :"
	@echo ""
	@echo "  make validate         Valide tout le workspace (schemas + semantic checks)"
	@echo "  make validate-strict  Idem, exit 1 si HIGH ou CRITICAL (pour hooks/CI)"
	@echo "  make validate-deep    Idem avec output JSON complet dans _validation-report.json"
	@echo "  make audit-substrate  Audit fraicheur + coherence du substrat encode (advisory)"
	@echo ""
	@echo "  make install-hook     Installe le pre-commit hook local (.git/hooks/pre-commit)"
	@echo "  make uninstall-hook   Désinstalle le pre-commit hook"
	@echo ""

validate:
	@python3 resources/scripts/validate-all.py

validate-strict:
	@python3 resources/scripts/validate-all.py --strict

validate-deep:
	@python3 resources/scripts/validate-all.py --deep --json _validation-report.json

audit-substrate:
	@python3 resources/scripts/audit-substrate.py --root .

install-hook:
	@GIT_ROOT=$$(git rev-parse --show-toplevel 2>/dev/null); \
	if [ -z "$$GIT_ROOT" ]; then \
		echo "✗ Pas dans un repo git. Lance cette commande depuis un repo initialisé."; \
		exit 1; \
	fi; \
	HOOK_PATH="$$GIT_ROOT/.git/hooks/pre-commit"; \
	cp resources/scripts/pre-commit.sh "$$HOOK_PATH"; \
	chmod +x "$$HOOK_PATH"; \
	echo "✓ Pre-commit hook installé : $$HOOK_PATH"

uninstall-hook:
	@GIT_ROOT=$$(git rev-parse --show-toplevel 2>/dev/null); \
	if [ -z "$$GIT_ROOT" ]; then \
		echo "✗ Pas dans un repo git."; \
		exit 1; \
	fi; \
	HOOK_PATH="$$GIT_ROOT/.git/hooks/pre-commit"; \
	if [ -f "$$HOOK_PATH" ]; then \
		rm "$$HOOK_PATH"; \
		echo "✓ Pre-commit hook supprimé"; \
	else \
		echo "✗ Aucun pre-commit hook installé"; \
	fi

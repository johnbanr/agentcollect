.PHONY: install test audit hack scrape clean

install:
	pip install -e ".[dev]"

test:
	pytest -q

audit:
	@test -n "$(COMPANY)" || (echo "Usage: make audit COMPANY=ooma.com" && exit 1)
	agentcollect-audit run https://$(COMPANY)

hack:
	@test -n "$(COMPANY)" || (echo "Usage: make hack COMPANY='Ooma' PHONE=+18669396662" && exit 1)
	agentcollect-audit hack "$(COMPANY)" --phone "$(PHONE)" --persona smb-phone

scrape:
	@test -n "$(COMPANY)" || (echo "Usage: make scrape COMPANY=ooma.com" && exit 1)
	agentcollect-audit scrape https://$(COMPANY)

clean:
	rm -rf output/ build/ dist/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +

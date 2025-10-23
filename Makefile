# Makefile for FormDetails Tool
# 簡化常用的開發命令

.PHONY: help install install-dev lint format check test clean pre-commit-install pre-commit-run merge optimize process-all

help:  ## 顯示幫助訊息
	@echo "可用的命令："
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## 安裝專案依賴
	pip install -e .

install-dev:  ## 安裝開發依賴
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

lint:  ## 執行程式碼檢查
	ruff check src/ tests/
	mypy src/ tests/

format:  ## 格式化程式碼
	ruff format src/ tests/
	black src/ tests/
	isort src/ tests/

format-check:  ## 檢查程式碼格式（不修改檔案）
	ruff format --check src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

check: lint format-check  ## 執行所有檢查（不修改檔案）

test:  ## 執行測試
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

test-watch:  ## 監聽模式執行測試
	pytest-watch tests/

security:  ## 執行安全性檢查
	safety check
	bandit -r . -f json -o bandit-report.json

clean:  ## 清理暫存檔案
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf out/
	rm -f *.log

merge:  ## 執行 JSON 合併
	python -m formdetails_tool merge

optimize:  ## 執行 C# 結構優化
	python -m formdetails_tool optimize

process-all:  ## 執行完整處理流程
	python -m formdetails_tool all

pre-commit-install:  ## 安裝 pre-commit hooks
	pre-commit install

pre-commit-run:  ## 執行 pre-commit 檢查
	pre-commit run --all-files

ci: check test security  ## 執行 CI 檢查（lint + test + security）

all: install-dev pre-commit-install  ## 完整設定開發環境

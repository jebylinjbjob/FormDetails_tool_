# Makefile for FormDetails Tool
# 簡化常用的開發命令

.PHONY: help install install-dev lint format check test clean pre-commit-install pre-commit-run

help:  ## 顯示幫助訊息
	@echo "可用的命令："
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## 安裝專案依賴
	pip install -e .

install-dev:  ## 安裝開發依賴
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

lint:  ## 執行程式碼檢查
	ruff check .
	mypy .

format:  ## 格式化程式碼
	ruff format .
	black .
	isort .

format-check:  ## 檢查程式碼格式（不修改檔案）
	ruff format --check .
	black --check .
	isort --check-only .

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

pre-commit-install:  ## 安裝 pre-commit hooks
	pre-commit install

pre-commit-run:  ## 執行 pre-commit 檢查
	pre-commit run --all-files

ci: check test security  ## 執行 CI 檢查（lint + test + security）

all: install-dev pre-commit-install  ## 完整設定開發環境

# Variables
PYTHON_FILES := $(shell find . -name "*.py")
APP_NAME := app/main.py

.PHONY: help install run shell clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies using pipenv"
	@echo "  make run          - Run the Streamlit dashboard"
	@echo "  make shell        - Enter the pipenv virtual environment"
	@echo "  make clean        - Remove python cache files"
	@echo "  make docker-build - Build Docker image (f1-driver-stats)"
	@echo "  make docker-run   - Run Docker image on port 8501"

install:
	pipenv install

run:
	PYTHONPATH=. pipenv run streamlit run $(APP_NAME)

shell:
	pipenv shell

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	pipenv requirements > requirements.txt
	docker build -t f1-driver-stats .
	@echo "Build complete. Image tagged as f1-driver-stats:latest"

docker-run:
	docker run -p 8501:8501 f1-driver-stats


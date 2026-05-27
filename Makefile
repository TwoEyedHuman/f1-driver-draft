# Variables
PYTHON_FILES := $(shell find . -name "*.py")
APP_NAME := app.py

.PHONY: help install run shell clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies using pipenv"
	@echo "  make run        - Run the Streamlit dashboard"
	@echo "  make shell      - Enter the pipenv virtual environment"
	@echo "  make clean      - Remove python cache files"

install:
	pipenv install

run:
	pipenv run streamlit run $(APP_NAME)

shell:
	pipenv shell

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	pipenv requirements > requirements.txt
	docker buildx build --platform linux/arm64 -t f1-auction-app:latest --load .
	@echo "Build complete. Image tagged as f1-auction-app:latest"


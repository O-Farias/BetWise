#!/bin/bash

# Ativa o ambiente virtual
source backend/venv/bin/activate

# Sobe o servidor com Uvicorn
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

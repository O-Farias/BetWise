from fastapi import FastAPI
from .routes import router  # Importa as rotas

app = FastAPI()

# Inclui as rotas do routes.py
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"mensagem": "Backend está rodando!"}

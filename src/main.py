from fastapi import FastAPI

from src.config.settings import obter_configuracoes

config = obter_configuracoes()

app = FastAPI(title="PDV Backend")



@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "ambiente": config.ambiente}
from fastapi import FastAPI

from src.config.settings import obter_configuracoes
from src.modules.catalogo.api.rotas import router as produtos_router
from src.modules.catalogo.api.rotas import router_ingredientes

config = obter_configuracoes()

app = FastAPI(title="PDV Backend")
app.include_router(produtos_router)
app.include_router(router_ingredientes)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "ambiente": config.ambiente}
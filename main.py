from fastapi import FastAPI, HTTPException, Depends, Form
from typing import List, Dict
from app.auth import verify_token
from app.data_processing import get_data_from_csv_files
import logging

# Configuração básica do FastAPI
app = FastAPI(
    title="API de Exemplo",
    description="API com autenticação JWT",
    version="1.0",
)

# Armazenar os dados em memória para evitar múltiplos downloads
data_cache = {}

@app.get("/producao", response_model=List[Dict])
def get_producao(token: str):
    try:
        logger.info("Recebendo requisição para /producao")
        verify_token(token)  # Verifica o token que veio via query string
        if "producao" not in data_cache:
            data_cache["producao"] = get_data_from_csv_files()  # Baixa e converte os dados
        logger.info("Dados de produção retornados com sucesso.")
        return data_cache["producao"]["producao"]
    except Exception as e:
        logger.error(f"Erro ao processar /producao: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar a requisição: {e}")

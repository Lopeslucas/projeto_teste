from fastapi import HTTPException
import jwt
from app.config import SECRET_KEY, ALGORITHM
import logging

logger = logging.getLogger(__name__)

def verify_token(token: str):
    try:
        logger.info(f"Tentando verificar o token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Token verificado com sucesso, payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token expirado")
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.PyJWTError as e:
        logger.error(f"Erro ao decodificar o token: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")

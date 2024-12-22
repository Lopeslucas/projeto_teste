import os
import requests
import pandas as pd
import json
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

# Função para baixar o arquivo CSV
def download_csv(url, file_path):
    try:
        logger.info(f"Iniciando download do arquivo: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Garante que o status da resposta é 2xx (sucesso)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Arquivo {file_path} baixado com sucesso.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao baixar o arquivo {url}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao baixar o arquivo: {e}")

# Função para converter CSV para JSON e salvar em arquivo
def convert_csv_to_json(file_path):
    try:
        logger.info(f"Convertendo o arquivo {file_path} de CSV para JSON.")
        # Lê o arquivo CSV usando pandas
        df = pd.read_csv(file_path, on_bad_lines='skip')  # Ignora linhas problemáticas
        json_data = df.to_dict(orient='records')  # Converte para lista de dicionários
        logger.info(f"Arquivo {file_path} convertido para JSON com sucesso.")
        
        # Salvar o JSON convertido em um arquivo
        json_file_path = file_path.replace('.csv', '.json')  # Nome do arquivo JSON
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)  # Salva o JSON em formato legível
        logger.info(f"Arquivo JSON salvo com sucesso em {json_file_path}.")
        
        return json_data  # Retorna os dados convertidos
    except Exception as e:
        logger.error(f"Erro ao converter o arquivo {file_path} para JSON: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao converter o arquivo para JSON: {e}")

# Função para baixar e converter todos os arquivos CSV
def get_data_from_csv_files():
    urls = {
        "producao": "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv",
        "processamento": "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv",
        "comercializacao": "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv",
        "importacao": "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv",
        "exportacao": "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"
    }
    os.makedirs("data", exist_ok=True)
    data = {}
    for key, url in urls.items():
        file_path = f"data/{key}.csv"
        download_csv(url, file_path)  # Baixa o arquivo
        data[key] = convert_csv_to_json(file_path)  # Converte para JSON e armazena
    return data

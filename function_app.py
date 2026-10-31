import azure.functions as func
import logging
import pdfplumber as pdf
import pandas as pd
import os
from pathlib import Path
from io import BytesIO
import json
import uuid

app = func.FunctionApp()

def open_pdf(file):
    arquivo = pdf.open(file)
    logging.info("PDF aberto com sucesso")
    return arquivo

def extract_tables_in_pdf(file):
    tables = []
    qtd_paginas = 0
    for i, pagina in enumerate(file.pages):
        if pagina.extract_table() != None:
            tables.append(pagina.extract_table())
            qtd_paginas += 1
    logging.info(f"Quantidade de páginas processadas: {qtd_paginas}")

    return tables

def normalize_data(tables):
    
    dicionario = []

    if len(tables) > 1:
        products = tables[0][5][0].split("\n")
        products += tables[1][0][0].split("\n")
    else:
        products = tables[0][5][0].split("\n")
    
    for item in products:
        separar = item.split()
        codigo = separar[0]
        descricao = " ".join(separar[1:-4])
        qtd = separar[-4]
        unidade = separar[-3]
        valor_unitario = separar[-2]
        valor_total = separar[-1]
        rowKey = str(uuid.uuid4())
        dicionario.append({
            "PartitionKey": "item_nota_fiscal",
            "RowKey": rowKey,
            "codigo": codigo,
            "descricao": descricao,
            "qtd": qtd,
            "unidade": unidade,
            "valor_unitario": valor_unitario,
            "valor_total": valor_total
        })
    logging.info("Dados normalizados com sucesso")
    return dicionario

@app.function_name(name="BlobTrigger1")
@app.blob_trigger(
    arg_name="myblob", 
    path="leituranotafiscal/arquivo.pdf",
    connection="AzureWebJobsStorage",
)
@app.table_output(arg_name="outputTable", table_name="NotaFiscal", connection="TableConnection")
def leitura_nota_fiscal(myblob: func.InputStream, outputTable: func.Out[str]):
    blob_content = myblob.read()
    buffer = BytesIO(blob_content)
    
    try:
        file = open_pdf(buffer)
        tables = extract_tables_in_pdf(file)
        data = normalize_data(tables)
        table_json = json.dumps(data)
        outputTable.set(table_json)
        logging.info("Dados exportados para a tabela com sucesso")
    except Exception as e:
        logging.error(f"Erro: {type(e).__name__} - {e}")
    finally:
        buffer.close()
        myblob.close()
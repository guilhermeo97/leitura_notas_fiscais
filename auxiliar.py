# import azure.functions as func
# import logging
# import pdfplumber as pdf
# import pandas as pd
# import os
# from pathlib import Path
# from io import BytesIO

# app = func.FunctionApp()

# def open_pdf(file):
#     arquivo = pdf.open(file)
#     logging.info("PDF aberto com sucesso")
#     return arquivo

# def extract_tables_in_pdf(file):
#     tables = []

#     for pagina in file.pages:
#         if pagina.extract_table() != None:
#             tables.append(pagina.extract_table())
#     #print(tables)
#     return tables

# def normalize_data(tables):
    
#     dicionario = []

#     if len(tables) > 1:
#         products = tables[0][5][0].split("\n")
#         products += tables[1][0][0].split("\n")
#     else:
#         products = tables[0][5][0].split("\n")
    
#     for item in products:
#         separar = item.split()
#         codigo = separar[0]
#         descricao = " ".join(separar[1:-4])
#         qtd = separar[-4]
#         unidade = separar[-3]
#         valor_unitario = separar[-2]
#         valor_total = separar[-1]
#         dicionario.append({
#             "codigo": codigo,
#             "descricao": descricao,
#             "qtd": qtd,
#             "unidade": unidade,
#             "valor_unitario": valor_unitario,
#             "valor_total": valor_total
#         })
#     print(dicionario)
#     return dicionario
    

# def export_to_excel(data, filename):
#     df_novo = pd.DataFrame(data)

#     if os.path.exists(filename):
#         df_existente = pd.read_excel(filename)
#         df_novo = df_novo[df_existente.columns.intersection(df_novo.columns)]
#         df_final = pd.concat([df_existente, df_novo], ignore_index=True)
#     else:
#         df_final = df_novo

#     df_final.to_excel(filename, index=False, merge_cells=True)

#     return "Linhas carregaddas com sucesso"

# @app.function_name(name="BlobTrigger1")
# @app.blob_trigger(arg_name="myblob", path="leituranotafiscal/arquivo.pdf",
#                                connection="AzureWebJobsStorage",
#                                ) 
# def leitura_nota_fiscal(myblob: func.InputStream):
#     logging.info(f"Python blob trigger function processed blob"
#                 f"Name: {myblob.name}\n"
#                 f"Blob Size: {myblob.length} bytes"
#             )
#     blob_content = myblob.read()
#     buffer = BytesIO(blob_content)
    
    
#     # Exemplo: processar o texto do blob
#     # text = blob_content.decode('utf-8')
#     # logging.info(f"Conteúdo: {text[:100]}...")
#     try:
#         #myblob.seek(0)  # Volta para o início do arquivo
#         file = open_pdf(buffer)
#         tables = extract_tables_in_pdf(file)
#         data = normalize_data(tables)
#         logging.info(data)
#     except Exception as e:
#         logging.error(f"Erro: {e}")

# # This example uses SDK types to directly access the underlying BlobClient object provided by the Blob storage trigger.
# # To use, uncomment the section below and add azurefunctions-extensions-bindings-blob to your requirements.txt file
# # Ref: aka.ms/functions-sdk-blob-python
# #
# # import azurefunctions.extensions.bindings.blob as blob
# # @app.blob_trigger(arg_name="client", path="leituranotafiscal",
# #                   connection="673910_STORAGE")
# # def leitura_nota_fiscal(client: blob.BlobClient):
# #     logging.info(
# #         f"Python blob trigger function processed blob \n"
# #         f"Properties: {client.get_blob_properties()}\n"
# #         f"Blob content head: {client.download_blob().read(size=1)}"
# #     )

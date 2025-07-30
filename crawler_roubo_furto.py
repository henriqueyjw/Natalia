import requests
from datetime import date
from bs4 import BeautifulSoup
from urllib.parse import quote
from tqdm import tqdm
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd

# Remove warnings a cada requisição
warnings.simplefilter('ignore', InsecureRequestWarning)

# Função principal para extração
def extract_decisoes_tjsp_grau1(links):
    dados = []  # Lista para armazenar os dados
    
    for link in links:
        session = requests.Session()
        req = session.get(link, verify=False)
        
        if "Não foi encontrado nenhum resultado correspondente à busca realizada" in req.text:
            print(f"Nenhum resultado encontrado para a URL: {link}")
            continue

        soupPrincipal = BeautifulSoup(req.content, 'html.parser')

        # Recupera o número total de resultados
        totalResultados = int(soupPrincipal.find("div", {"id": "resultados"}).find_all("table")[0].tr.td.text.strip().split("de ")[1])
        totalPaginas = totalResultados // 10 if totalResultados % 10 == 0 else (totalResultados // 10) + 1
        
        print(f"Iniciando coleta de dados para a URL: {link}")
        for i in tqdm(range(1, totalPaginas + 1)):
            url_paginate = f"https://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=roubo+OU+furto&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.nuProcesso=&dadosConsulta.nuProcessoAntigo=&classeTreeSelection.values=&classeTreeSelection.text=&assuntoTreeSelection.values=&assuntoTreeSelection.text=&agenteSelectedEntitiesList=&contadoragente=0&contadorMaioragente=0&cdAgente=&nmAgente=&dadosConsulta.dtInicio=01%2F01%2F2021&dadosConsulta.dtFim=31%2F12%2F2021&varasTreeSelection.values=&varasTreeSelection.text=&dadosConsulta.ordenacao=DESC"
            req = session.get(url_paginate, verify=False)
            soupPrincipal = BeautifulSoup(req.content, 'html.parser')
            
            for target in soupPrincipal.find_all('tr', {'class': 'fundocinza1'}):
                contador = 0
                linha = {
                    "numero_cnj": None,
                    "classe": None,
                    "assunto": None,
                    "magistrado": None,
                    "comarca": None,
                    "foro": None,
                    "vara": None,
                    "data_disponibilizacao": None,
                    "decisao": None,
                }

                for info in target.find_all('tr', {'class': 'fonte'}):
                    if contador == 0:
                        linha["numero_cnj"] = info.span.text.strip()
                    elif contador == 1:
                        linha["classe"] = info.td.text.strip().split("\n\t")[-1].strip()
                    elif contador == 2:
                        linha["assunto"] = info.td.text.strip().split("\n\t")[-1].strip()
                    elif contador == 3:
                        linha["magistrado"] = info.td.text.strip().split("\n\t")[-1].strip()
                    elif contador == 4:
                        linha["comarca"] = info.td.text.strip().split("\n\t")[-1].strip()
                    elif contador == 5:
                        linha["foro"] = info.td.text.strip().split("\n\t")[-1].strip()
                    elif contador == 6:
                        linha["vara"] = info.td.text.strip().split("\n\t")[-1].strip()
                    elif contador == 7:
                        linha["data_disponibilizacao"] = info.td.text.strip().split("\n\t")[-1].strip()
                    elif contador == 8:
                        linha["decisao"] = info.td.find_all('div', {'style': 'display: none;'})[-1].span.text.strip()

                    contador += 1

                dados.append(linha)  # Adiciona a linha aos dados

    # Retorna os dados como um DataFrame
    # pd.DataFrame(dados).to_excel(f"decisoes_tjsp_{date.today()}.xlsx", index=False)
    return pd.DataFrame(dados)



# Lista de links
# Execução

import pandas as pd

input_data = pd.read_excel('dados_sentencas.xlsx')
input_data.input2 = input_data.PROCESSO.str[-4:]
links = list()
df = pd.DataFrame()
for _,row in input_data.iterrows():
    link = f'https://esaj.tjsp.jus.br/cjpg/pesquisar.do;jsessionid=A3B093BF00038BA60208A3DFE512B566.cjpg1?conversationId=&dadosConsulta.pesquisaLivre=&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado={row.input1}&foroNumeroUnificado={row.input2}&dadosConsulta.nuProcesso={row.PROCESSO}&dadosConsulta.nuProcessoAntigo=&classeTreeSelection.values=&classeTreeSelection.text=&assuntoTreeSelection.values=&assuntoTreeSelection.text=&agenteSelectedEntitiesList=&contadoragente=0&contadorMaioragente=0&cdAgente=&nmAgente=&dadosConsulta.dtInicio=&dadosConsulta.dtFim=&varasTreeSelection.values=&varasTreeSelection.text=&dadosConsulta.ordenacao=DESC'
    links.append(link)
df = extract_decisoes_tjsp_grau1(links)
df.to_excel(f"decisoes_tjsp_{date.today()}.xlsx", index=False)
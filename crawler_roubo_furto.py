import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import time
import re
import pandas as pd

path = 'C:/Users/henri/Desktop/programs'
final_path = 'E:/artigo3/dados_crime'

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=800,600")
driver = webdriver.Chrome(executable_path = os.path.join(path,'chromedriver.exe'), options = chrome_options)

links = [
    'https://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=roubo+OU+furto&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.nuProcesso=&dadosConsulta.nuProcessoAntigo=&classeTreeSelection.values=&classeTreeSelection.text=&assuntoTreeSelection.values=&assuntoTreeSelection.text=&agenteSelectedEntitiesList=&contadoragente=0&contadorMaioragente=0&cdAgente=&nmAgente=&dadosConsulta.dtInicio=01%2F01%2F2021&dadosConsulta.dtFim=31%2F12%2F2021&varasTreeSelection.values=&varasTreeSelection.text=&dadosConsulta.ordenacao=DESC'
    ]

rows = list()
file_number = 27
for url in links:
    driver.get(url)
    for i in range(8000):
        html_source = driver.page_source
        soup = BeautifulSoup(html_source,"html.parser")
        for target in soup.find_all('tr',{'class':'fundocinza1'}):
            contador = 0
            flag = False
            linha = dict()
            for info in target.find_all('td',{'align':'left'})[1:]:
                if len(target.find_all('td',{'align':'left'})[1:]) == 8:
                    if contador == 0:
                        linha['numero_cnj'] = re.sub(r'\s{2,100}','',info.text)
                    elif contador == 1:
                        linha['classe'] = None
                        linha['assunto'] = re.sub(r'\s{2,100}','',info.text)[8:]
                    elif contador == 2:
                        linha['magistrado'] = re.sub(r'\s{2,100}','',info.text)[11:]
                    elif contador == 3:
                        linha['comarca'] = re.sub(r'\s{2,100}','',info.text)[8:]
                    elif contador == 4:
                        linha['foro'] = re.sub(r'\s{2,100}','',info.text)[5:]
                    elif contador == 5:
                        linha['vara'] = re.sub(r'\s{2,100}','',info.text)[5:]
                    elif contador == 6:
                        linha['data'] = re.sub(r'\s{2,100}','',info.text)[25:]
                    elif contador == 7:
                        linha['decisao'] = re.sub(r'[\n\t]{1,100}','',info.text)
                    contador += 1
                if len(target.find_all('td',{'align':'left'})[1:]) == 9:
                    if contador == 0:
                        linha['numero_cnj'] = re.sub(r'\s{2,100}','',info.text)
                    elif contador == 1:
                        linha['classe'] = re.sub(r'\s{2,100}','',info.text)[7:]
                    elif contador == 2:
                        linha['assunto'] = re.sub(r'\s{2,100}','',info.text)[8:]
                    elif contador == 3:
                        linha['magistrado'] = re.sub(r'\s{2,100}','',info.text)[11:]
                    elif contador == 4:
                        linha['comarca'] = re.sub(r'\s{2,100}','',info.text)[8:]
                    elif contador == 5:
                        linha['foro'] = re.sub(r'\s{2,100}','',info.text)[5:]
                    elif contador == 6:
                        linha['vara'] = re.sub(r'\s{2,100}','',info.text)[5:]
                    elif contador == 7:
                        linha['data'] = re.sub(r'\s{2,100}','',info.text)[25:]
                    elif contador == 8:
                        linha['decisao'] = re.sub(r'[\n\t]{1,100}',' ',info.text)
                    contador += 1
            rows.append(linha)
        try:
            if i == 0:
                driver.find_elements_by_xpath('//*[@id="resultados"]/table[3]/tbody/tr[1]/td[2]/div/a[5]')[0].click()
                time.sleep(4)
            else:
                driver.find_elements_by_xpath('//*[@id="resultados"]/table[1]/tbody/tr[1]/td[2]/div/a[6]')[0].click()
                time.sleep(4)
        except:
            break

    df = pd.DataFrame(rows).drop_duplicates()
    df.to_csv(os.path.join(final_path, f'banco_decisoes_paper3_comparison_{file_number}.csv'),index=False)
    rows = list()
    file_number += 1

driver.quit()

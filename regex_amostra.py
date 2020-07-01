import os, os.path, re, nltk
import pandas as pd
from nltk.util import everygrams

path = '/mnt/e/natalia/hc'
filename = 'Base_Amostra_Regex.xlsx'

df = pd.read_excel(os.path.join(path,filename)) # Abre arquivos em Excel
df = pd.read_csv(os.path.join(path,filename), error_bad_lines = False) # Abre arquivos em CSV

rows = []
lista = []
for _,row in df.iterrows():
    dicionario_df = dict()
    inicio = round(len(row['Texto'])/3)
    dicionario_df = {'Texto':row['Texto']}
    
    try:
        dicionario_df['Impetrante'] = re.findall(r'(?<=impetrante:\s)(.*?)(?=\s[–-])|(?<=impetrante\(s\):\s)(.*?)(?=\spaciente\(s\))',row['Texto'][:1000],re.IGNORECASE)[0]
    except:
        dicionario_df['Impetrante'] = ''

    try:
        dicionario_df['Magistrado'] = re.findall(r'(?<=magistrado\(a\)\s)(.*?)(?=\s[–-])',row['Texto'][-1000:],re.IGNORECASE)[0]
    except:
        dicionario_df['Magistrado'] = ''  
        
    try:
        dicionario_df['Data do julgamento'] = re.findall(r'\d{2}\sde\s\w{4,8}\sde\s\d{4}',row['Texto'][-1000:],re.IGNORECASE)[0]
    except:
        dicionario_df['Data do julgamento'] = ''
    
    rows.append(dicionario_df)
data_frame = pd.DataFrame(rows)
with pd.ExcelWriter(os.path.join(path, f'resultado_amostra.xlsx'),
                            engine='openpyxl',
                            mode='w') as writer:
            data_frame.to_excel(writer, index = False)

# freq = nltk.FreqDist(list(everygrams(lista, min_len = 3, max_len = 6)))
# df_fdist = pd.DataFrame.from_dict(freq, orient='index')
# df_fdist.columns = ['Frequency']
# df_fdist.index.name = 'Term'
# with pd.ExcelWriter(os.path.join(path, f'frequencia.xlsx'),
#                             engine='openpyxl',
#                             mode='w') as writer:
#             df_fdist.to_excel(writer)
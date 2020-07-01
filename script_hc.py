import os, os.path, re
import pandas as pd

path = '/mnt/e/natalia/hc'
filename = 'dados HC_Natalia27Maio.xlsx'

df = pd.read_excel(os.path.join(path, filename))
rows = []
lista = []

for _, row in df.iterrows():
    dicionario_df = dict()

# Informações iniciais incluídas nos dados finais

    dicionario_df = {
        'tribunal': row['Tribunal'],
        'numero_cnj': row['Numero'],
        'data_doe': row['Data_DOE'],
        'doe': row['DOE'],
        'texto': row['Texto'],
        'procedimento': row['Procedimento']
    }

# Classificação do resultado do processo indicado no texto observando os 1000 últimos caractéres

    resultadoProcesso = re.search(
        r'[\s,\.]denega[\s\-]{1,3}se\sassim\sa\sliminar|[\s,\.]n[aã]o\spode\so\spedido\sser\sdeferido|[\s,\.]indefiro|[\s,\.]nego\sseguimento|[\s,\.]julgo\sextinto|[\s,\.]ext[íi]nguo|[\s,\.]n[aã]o\sse\sconhece[r]|[\s,\.]n[aã]o\sconhe[cç]o|[\s,\.]indeferido\so\spedido|[\s,\.]inadequada\s[aà]\sesfera\sde\scogni[cç][aã]o\ssum[aá]ria|[\s,\.]mantenho\sa\sdecis[aã]o.{1,30}que\sindeferiu|[\s,\.]indefere[\s-]se|[\s,\.]n[aã]o\sse\smostra\srecomend[áa]vel\sa\sado[cç][aã]o|[\s,\.]ponto\sde\sensejar\sa\santecipa[cç][aã]o|[\s,\.]n[aã]o\sse\sedivisa\silegalidade\smanifesta|[\s,\.]n[aã]o\sse\sedivisa\sconstrangimento\silegal|[\s,\.]n[aã]o\sse\sedivisa\sflagrante\silegalidade|[\s,\.]seria\sprematuro\sreconhecer',
        row['Texto'][-1000:], re.IGNORECASE)
    resultadoProcessop = re.search(
        r'[\s,\.]expe[cç]a[\s-]se\salvar[aá]\sde\ssoltura|[\s,\.]defiro|[\s,\.]concedo|[\s,\.]dou\sprovimento|[\s,\.]provejo',
        row['Texto'][-1000:], re.IGNORECASE)
    resultadoProcessopp = re.search(
        r'[\s,\.]julgo\sparcialmente|[\s,\.]defiro\sparcialmente|[\s,\.]projeto\sparcialmente|[\s,\.]concedo\sparcialmente|[\s,\.]concedo\sem\sparte|[\s,\.]defiro\sem\sparte',
        row['Texto'][-1000:], re.IGNORECASE)

    if resultadoProcesso:
        dicionario_df['indeferido'] = 1
    else:
        dicionario_df['indeferido'] = 0
    if resultadoProcessopp:
        dicionario_df['parcialmente'] = 1
    else:
        dicionario_df['parcialmente'] = 0
    if resultadoProcessop:
        dicionario_df['provido'] = 1
    else:
        dicionario_df['provido'] = 0

    if not resultadoProcesso and not resultadoProcessopp and not resultadoProcessop:
        lista = lista + row['Texto'][-1000:].split()
        dicionario_df['desconhecido'] = 1
    else:
        dicionario_df['desconhecido'] = 0

# Busca por termos específicos para cidade, impetrante, impetrado, órgão julgador, relator e data

    try:
        dicionario_df['cidade'] = re.findall(
            r'(?<=\shabeas\scorpus\scriminal\s[–-]\s)(.*?)(?=\s[–-])|(?<=\s{2}habeas\s{2}corpus\s{2}criminal\s{2}[–-]\s{2})(.*?)(?=\s[–-])',
            row['Texto'][:1000], re.IGNORECASE)[0]
    except:
        dicionario_df['cidade'] = ''

    try:
        dicionario_df['impetrante'] = re.findall(
            r'(?<=impetrante:\s)(.*?)(?=\s[–-])|(?<=impetrante\(s\):\s)(.*?)(?=\spaciente\(s\))',
            row['Texto'][:1000], re.IGNORECASE)[0]
    except:
        dicionario_df['impetrante'] = ''

# Padrão de identificação do relator no início do texto (1000 caractéres iniciais)
    try:
        dicionario_df['relator_1'] = re.findall(
            r'(?<=relator\(a\):\s)(.*?)(?=\s[oó]rg[aã]o\sjulgador:\s)|(?<=relator\(a\):\s{2})(.*?)(?=\s{2}[oó]rg[aã]o\s{2}julgador:\s)',
            row['Texto'][:1000], re.IGNORECASE)[0]
    except:
        dicionario_df['relator_1'] = ''

    try:
        dicionario_df['org_julgador'] = re.findall(
            r'(?<=[oó]rg[aã]o\sjulgador:\s)(.*?)(?=\simpetrante\(s\))|(?<=ju[ií]z\sde\sdireito\s{2}d[ea]\s)(.*?)(?=,)|(?<=ju[ií]z\s{2}de\s{2}direito\s{2}d[ea]\s{2})(.*?)(?=,)',
            row['Texto'][:1000], re.IGNORECASE)[0]
    except:
        dicionario_df['org_julgador'] = ''

    try:
        dicionario_df['paciente'] = re.findall(
            r'(?<=paciente:\s)(.*?)(?=\s[–-])|(?<=paciente:\s{2})(.*?)(?=\s[–-])',
            row['Texto'][:1000], re.IGNORECASE)[0]
    except:
        dicionario_df['paciente'] = ''

    try:
        dicionario_df['data'] = re.findall(r'\d{2}\sde\s\w{4,8}\sde\s\d{4}',
                                           row['Texto'][-1000:],
                                           re.IGNORECASE)[0]
    except:
        dicionario_df['data'] = ''

# Padrão de identificação do relator no final do texto (1000 caractéres finais)
    try:
        dicionario_df['relator_2'] = re.findall(
            r'(?<=magistrado\(a\)\s)(.*?)(?=\s[–-])', row['Texto'][-1000:],
            re.IGNORECASE)[0]
    except:
        dicionario_df['relator_2'] = ''

    rows.append(dicionario_df)
data_frame = pd.DataFrame(rows)

# Salvando os dados em um arquivo excel
with pd.ExcelWriter(os.path.join(path, f'resultado_27_05.xlsx'),
                    engine='openpyxl',
                    mode='w') as writer:
    data_frame.to_excel(writer, index=False)

# Extra: Indica as frases mais frequentes com 3 a 6 palavras

# import nltk
# freq = nltk.FreqDist(list(everygrams(lista, min_len = 3, max_len = 6)))
# df_fdist = pd.DataFrame.from_dict(freq, orient='index')
# df_fdist.columns = ['Frequency']
# df_fdist.index.name = 'Term'
# with pd.ExcelWriter(os.path.join(path, f'frequencia.xlsx'),
#                             engine='openpyxl',
#                             mode='w') as writer:
#             df_fdist.to_excel(writer)

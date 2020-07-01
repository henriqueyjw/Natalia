import os
import os.path
import pyreadr
import pandas as pd

PATH = '/mnt/d/previdencia_metadados'
ASSUNTOS = ['6114', '11946', '11947']
FILENAME = "insper.RData"

RESULT = pyreadr.read_r(os.path.join(PATH, FILENAME))
DF = RESULT["insper"]
# DF.drop_duplicates(subset="id", keep=False, inplace=True)
NEW = DF["id"].str.split("_", n=4, expand=True)
DF["n_processo"] = NEW[4]
DF['ano'] = DF["n_processo"].str[9:13]
DF['tribunal'] = NEW[0]
DF['ramo_justica'] = DF["n_processo"].str[13:14]
DF['comarca'] = DF["n_processo"].str[16:18]

ESTADOS = {
    '30':'AC', '80':'AL', '31':'AP', '32':'AM',
    '33':'BA', '81':'CE', '34':'DF', '50':'ES',
    '35':'GO', '37':'MA', '36':'MT', '60':'MS',
    '38':'MG', '39':'PA', '82':'PB', '70':'PR',
    '83':'PE', '40':'PI', '51':'RJ', '84':'RN',
    '71':'RS', '41':'RO', '42':'RR', '72':'SC',
    '61':'SP', '85':'SE', '43':'TO'
}

for subj in ASSUNTOS:
    NEW_DF = DF[DF.assuntos == subj]
    ESTADO_INICIAL = ['vazio'] * len(NEW_DF)
    NEW_DF['estado'] = ESTADO_INICIAL
    for _,row in NEW_DF.iterrows():
        if row['ramo_justica'] == '4':
            try:
                row['estado'] = ESTADOS[row['comarca']]
            except:
                row['estado'] = 'NA'
        elif row['ramo_justica'] == '8':
            row['estado'] = row['tribunal'][-2:]

    FINAL = NEW_DF.groupby(['ano','estado']).size().reset_index(name="Time")
    with pd.ExcelWriter(os.path.join(PATH, f'freq_bpc_{subj}.xlsx'),
                        engine='openpyxl',
                        mode='w') as writer:
        FINAL.to_excel(writer, index=False)

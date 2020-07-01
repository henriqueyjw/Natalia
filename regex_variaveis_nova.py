import os, os.path, re
import pandas as pd

path = '/mnt/e/natalia/hc'
filename = 'dados_total.xlsx'

df = pd.read_excel(os.path.join(path,filename)) # Abre arquivos em Excel
rows = []

dicionario_termos = {
    'recomendacao_62':r'[\.,\s]recomenda[ça][ãa]o\s62|[\.,\s]recomenda[ça][ãa]o\scnj|[\.,\s]recomenda[ça][ãa]o\sn.?\s62|[\.,\s]recomenda[ça][ãa]o\sdo\sConselho\sNacional\sde\sJusti[cç]a|[\.,\s]recomenda[ça][ãa]o\sdo\scnj',
    'recomendacao':r'[\.,\s]recomenda[ça][ãa]',
    'vga_roubo':r'[\.,\s]roubo|[\.,\s]art.?\s157|artigo\s157',
    'vga_homicidio':r'[\.,\s]homic[íi]dio|[\.,\s]art.?\s121|artigo\s121',
    'vga_ameaca':r'[\.,\s]amea[cç]a|[\.,\s]art.?\s147|artigo\s147',
    'vga_lesao':r'[\.,\s]les[aã]o\scorporal|[\.,\s]art.?\s129|artigo\s129',
    'vga_est':r'[\.,\s]estupro|[\.,\s]art.?\s213|artigo\s213',
    'vga_latr':r'[\.,\s]latroc[í]nio|[\.,\s]art.?\s217|artigo\s217',
    'vga_ext':r'[\.,\s]extors[ãa]o|[\.,\s]art.?\s158|artigo\s158',
    'vga_seq':r'[\.,\s]sequestro|[\.,\s]art.?\s159|artigo\s159',
    'vga_fem':r'[\.,\s]feminic[íi]dio|[\.,\s]art.?\s124|artigo\s124',
    'vga_abort':r'[\.,\s]aborto|[\.,\s]art.?\s125|artigo\s125',
    'vga_medida':r'descumprimento\sde\smedida\sprotetiva',
    'grupo_risco':r'grupo[s]?\sde\srisco',
    'grupo_idosos':r'idos[ao][s]?',
    'grupo_hiv':r'hiv|aids|aid[ée]tico|portador\s\de\simunodefici[êe]ncia',
    'grupo_resp':r'doen[cç]a[s]?\srespirat[oó]ria[s]?',
    'grupo_matern':r'[\.,\s]m[aã]e|gravidez|gr[aá]vida|maternidade|[\.,\s]gestante',
    'grupo_infecc':r'[\.,\s]coinfec[cç][aã]o|[\.,\s]coinfec[cç][oõ]es',
    'grupo_imunossup':r'[\.,\s]doen[cç]a[s]?\simunossupressora[s]?',
    'grupo_doencas':r'[\.,\s]tuberculose|[\.,\s]asma|[\.,\s]diabetes|[\.,\s]doen[cç]a[s]?\srena[lais]{1,3}|[\.,\s]doen[cç]a[s]?\scr[oô]nica[s]?',
    'grupo_comorb':r'[\.,\s]comorbidade[s]?',
    'grupo_lact':r'[\.,\s]lactante[s]?',
    'grupo_hipert':r'[\.,\s]hipertens[aã]o|hipertens[oa][s]?',
    'grupo_resp_menor':r'[\.,\s]respons[aá]vel\spor\scrian[cç]a[s]?|[\.,\s]respons[aá]veis\spor\scrian[cç]a[s]?|[\.,\s]respons[aá]vel\spor\smenor[es]{0,2}\sde\sidade|[\.,\s]respons[aá]veis\spor\smenor[es]{0,2}\sde\sidade',
    'grupo_resp_def':r'[\.,\s]respons[aá]vel\spor\spessoa[s]?\scom\sdefici[eê]ncia|[\.,\s]respons[aá]veis\spor\spessoa[s]?\scom\sdefici[eê]ncia',
    'indigenas':r'[\.,\s][ií]ndio[s]?|[\.,\s]ind[íi]gena[s]?',
    'adolescentes':r'[\.,\s]adolescente[s]|[\.,\s]adolescente[s]\scom\sdefici[eê]ncia',
    'adpf_347':r'[\.,\s]adpf\s347|ministro\smarco\saur[eé]lio|argui[cç][aã]o\sde\sdescumprimento\sfundamental\sn.?\s?347|estado\sde\scoisas\sinconstitucional'
}
for _,row in df.iterrows():
    dici = dict()
    dici['tribunal']=row.tribunal
    dici['numero_cnj']=row.numero_cnj
    dici['data_doe']=row.data_doe
    dici['doe']=row.doe
    dici['texto']=row.texto
    dici['procedimento']=row.procedimento
    dici['cidade']=row.cidade
    dici['impetrante']=row.impetrante
    dici['org_julgador']=row.org_julgador
    dici['paciente']=row.paciente
    dici['data']=row.data
    dici['relator_2']=row.relator_2
    dici['indeferido']=row.indeferido
    dici['parcialmente']=row.parcialmente
    dici['provido']=row.provido
    dici['desconhecido']=row.desconhecido
    dici['sem_decisao']=row.sem_decisao
    dici['prejudicad']=row.prejudicad
#     dici['resolucao62']=row.resolucao62
#     dici['grupo_risco']=row.grupo_risco
#     dici['adpf347']=row.adpf347
    dici['defensoria']=row.defensoria
    for k, v in dicionario_termos.items():
        if re.search(v, row.texto, re.S | re.I):
            place = re.search(v,row.texto, re.S | re.I).span()
            dici[k] = row.texto[place[0]-600:place[1]+600]
            # dici[k] = 1
        else:
            dici[k] = 0
    rows.append(dici)
DATA_FRAME = pd.DataFrame(rows)
with pd.ExcelWriter(os.path.join(path, f'dados_total.xlsx'),
                            engine='openpyxl',
                            mode='w') as writer:
            DATA_FRAME.to_excel(writer, index = False)
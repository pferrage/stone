import numpy as np
import pandas as pd
import src.tools.utils as ut

def getAllRecordsFromABronzeTable(tabName,dt):
    query = f'''
                select * from {tabName} where dat_ingestion = '{dt}'
             '''
    return ut.loadSQLToDataFrame(query, 'bronze')


# Função para chamar dinamicamente uma função com base no nome
def treatColumns(df,tabName):
    
    # Lista de tabelas
    tableList = {'tb_empresas': tb_empresas,
                     'tb_socios': tb_socios,
                     'tb_qualificacoes': tb_qualificacoes}

    if tabName in tableList:
        setTable = tableList[tabName]
        df = setTable(df)

        df.columns = [item.lower() for item in df.columns]
        return df
    else:
        raise ValueError(f"A tabela '{tabName}' não possui um De-Para configurado.")
    

def tb_empresas(df):
   
    df['cnpj']                     = df['0']
    df['razao_social']             = df['1']
    df['natureza_juridica']        = df['2'].astype(np.int64)
    df['qualificacao_responsavel'] = df['3'].astype(np.int64)
    df['capital_social']           = df['4'].str.replace(',', '.').astype(np.float64)
    df['cod_porte']                = df['5']
    df['dat_ingestion']            = pd.to_datetime(df['dat_ingestion'])

    df = df[['cnpj','razao_social','natureza_juridica','qualificacao_responsavel','capital_social','cod_porte','dat_ingestion']]
    return df

def tb_socios(df):

    df['cnpj']                      = df['0']
    df['tipo_socio']                = df['1'].astype(np.int64)
    df['nome_socio']                = df['2']
    df['documento_socio']           = df['3']
    df['codigo_qualificacao_socio'] = df['4']
    df['dat_ingestion']             = pd.to_datetime(df['dat_ingestion'])

    df = df[['cnpj','tipo_socio','nome_socio','documento_socio','codigo_qualificacao_socio','dat_ingestion']]
    return df
    


def tb_qualificacoes(df):
  
    df['id']        = df['0'].astype(int)
    df['descricao'] = df['1']
    df['dat_ingestion'] = pd.to_datetime(df['dat_ingestion'])
    
    df = df[['id','descricao','dat_ingestion']]
    return df
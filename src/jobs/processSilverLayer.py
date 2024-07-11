import pandas as pd
import tools.utils as ut


def processSilverLayer(tabName,dt):
    df = getAllRecordsFromABronzeTable(tabName,dt)
    df = treatColumns(df,tabName)

    df = df.drop_duplicates()
    ut.loadDataFrameToSQL(df,tabName,'silver')

def getAllRecordsFromABronzeTable(tabName: str,dt: object) -> tuple[pd.DataFrame]:
    query = f'''
                select * from {tabName} where dat_ingestion = '{dt}'
             '''
    return ut.loadSQLToDataFrame(query, 'bronze')

def treatColumns(df: pd.DataFrame, tabName: str) -> tuple[pd.DataFrame]:
    tableList = {'tb_empresas': tb_empresas,
                 'tb_socios': tb_socios,
                 'tb_qualificacoes': tb_qualificacoes}

    if tabName in tableList:
        setTable = tableList[tabName]
        df = setTable(df)

        df.columns = [item.lower() for item in df.columns]
        return df
    else:
        raise ValueError(f"The table '{tabName}' doen't have a From-To configured.")
    

def tb_empresas(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    df['cnpj']                     = df['0']
    df['razao_social']             = df['1']
    df['natureza_juridica']        = df['2'].astype(int)
    df['qualificacao_responsavel'] = df['3'].astype(int)
    df['capital_social']           = df['4'].str.replace(',', '.')
    df['cod_porte']                = df['5']
    df['dat_ingestion']            = pd.to_datetime(df['dat_ingestion'])

    df = df[['cnpj','razao_social','natureza_juridica','qualificacao_responsavel','capital_social','cod_porte','dat_ingestion']]
    return df

def tb_socios(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    df['cnpj']                      = df['0']
    df['tipo_socio']                = df['1'].astype(int)
    df['nome_socio']                = df['2']
    df['documento_socio']           = df['3']
    df['codigo_qualificacao_socio'] = df['4']
    df['dat_ingestion']             = pd.to_datetime(df['dat_ingestion'])

    df = df[['cnpj','tipo_socio','nome_socio','documento_socio','codigo_qualificacao_socio','dat_ingestion']]
    return df
    


def tb_qualificacoes(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    df['id']            = df['0'].astype(int)
    df['descricao']     = df['1']
    df['dat_ingestion'] = pd.to_datetime(df['dat_ingestion'])
    
    df = df[['id','descricao','dat_ingestion']]
    return df
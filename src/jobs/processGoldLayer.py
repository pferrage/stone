import pandas as pd
import tools.utils as ut


def processGoldLayer(dt: object) -> tuple[None]:
    df_company = getAllRecordsFromASilverTable('tb_empresas')
    df_partner = getAllRecordsFromASilverTable('tb_socios')

    df,tabName = setVwEmpresaSocio(df_company,df_partner,dt)

    df = df.drop_duplicates()   
    df.update(df['qtde_socios'].fillna(0)) 
    df.update(df['doc_alvo'].fillna(False)) 
    df.update(df['flag_socio_estrangeiro'].fillna(False)) 
    
    ut.loadDataFrameToSQL(df,tabName,'gold')


def getAllRecordsFromASilverTable(tabName: str) -> pd.DataFrame:
    query = f'''
                select * from {tabName}
             '''
    return ut.loadSQLToDataFrame(query, 'silver')


def setVwEmpresaSocio(df_company: pd.DataFrame, df_partner: pd.DataFrame, dt: object) -> tuple[pd.DataFrame, str]:
    df_partners_by_company = df_partner.groupby('cnpj').size().reset_index(name='qtde_socios')

    df_foreign_partners = df_partner[df_partner['tipo_socio'] == 3].drop_duplicates('cnpj')
    df_foreign_partners['flag_socio_estrangeiro'] = True

    df_company_doc = df_company[df_company['cod_porte'] == 3][['cnpj']]
    df_multiple_partners = df_partners_by_company[df_partners_by_company['qtde_socios'] > 1][['cnpj']]
    flag_doc = pd.merge(df_company_doc, df_multiple_partners, on='cnpj')
    flag_doc['doc_alvo'] = True

    df = pd.merge(df_company[['cnpj']], df_partners_by_company, on='cnpj', how='left')
    df = pd.merge(df, df_foreign_partners[['cnpj', 'flag_socio_estrangeiro']], on='cnpj', how='left')
    df = pd.merge(df, flag_doc[['cnpj', 'doc_alvo']], on='cnpj', how='left')

    df['flag_socio_estrangeiro'].fillna(False, inplace=True)
    df['doc_alvo'].fillna(False, inplace=True)

    df[['dat_ingestion']] = dt
    
    return df,'tb_consolidado_socios'



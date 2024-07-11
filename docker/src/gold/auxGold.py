import pandas as pd
import tools.utils as ut

def setVwEmpresaSocio(df_emp, df_soc, dt):
  
    socios_por_empresa = df_soc.groupby('cnpj').size().reset_index(name='qtde_socios')


    socios_estrangeiros = df_soc[df_soc['tipo_socio'] == 3].drop_duplicates('cnpj')
    socios_estrangeiros['flag_socio_estrangeiro'] = True

    empresas_doc = df_emp[df_emp['cod_porte'] == 3][['cnpj']]
    socios_multiplos = socios_por_empresa[socios_por_empresa['qtde_socios'] > 1][['cnpj']]
    flag_doc = pd.merge(empresas_doc, socios_multiplos, on='cnpj')
    flag_doc['doc_alvo'] = True

    df = pd.merge(df_emp[['cnpj']], socios_por_empresa, on='cnpj', how='left')
    df = pd.merge(df, socios_estrangeiros[['cnpj', 'flag_socio_estrangeiro']], on='cnpj', how='left')
    df = pd.merge(df, flag_doc[['cnpj', 'doc_alvo']], on='cnpj', how='left')

    df['flag_socio_estrangeiro'].fillna(False, inplace=True)
    df['doc_alvo'].fillna(False, inplace=True)

    df[['dat_ingestion']] = dt
    
    return df,'tb_consolidado_socios'


def getAllRecordsFromASilverTable(tabName):
    query = f'''
                select * from {tabName}
             '''
    return ut.loadSQLToDataFrame(query, 'silver')


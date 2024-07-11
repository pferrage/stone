import tools.utils as ut
import gold.auxGold as aux


def processGoldLayer(dt):
    df_emp = aux.getAllRecordsFromASilverTable('tb_empresas')
    df_soc = aux.getAllRecordsFromASilverTable('tb_socios')

    df,tabName = aux.setVwEmpresaSocio(df_emp,df_soc,dt)

    df = df.drop_duplicates()   
    df.update(df['qtde_socios'].fillna(0)) 
    df.update(df['doc_alvo'].fillna(False)) 
    df.update(df['flag_socio_estrangeiro'].fillna(False)) 
    
    ut.loadDataFrameToSQL(df,tabName,'gold')

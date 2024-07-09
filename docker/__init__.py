
# coding: utf-8
# In[ ]:
import main as _main

def main():
    _main.processETL('empresas')
    _main.processETL('socios')
    #_main.processETL('qualifi')   ##Base menor, ideal para testes (EXCLUIR ANTES DE ENVIAR)

if __name__ == "__main__":
    main()
# %%

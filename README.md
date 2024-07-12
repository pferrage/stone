# Data engineer - Challenge

## Overview
Insights on data extracted from the Brazilian Federal Revenue Service's Open Data Portal. 
The data is available via the link: https://dadosabertos.rfb.gov.br/CNPJ/

## Data Processing Project
This project is responsible for downloading, processing and storing company and member data, dividing processing into three layers: bronze, silver and gold.
The process also allows for the storage of other data from the same public repository.

### Data project structure
/root/
├── src/
│ ├── jobs/
│ │ ├── processBronzeLayer.py
│ │ ├── processSilverLayer.py
│ │ ├── processGoldLayer.py
│ │ └── processDataQuality.py
│ ├── tools/
│ │ └── utils.py
└── main.py

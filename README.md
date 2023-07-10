# WebScraper de vagas de dados em grandes empresas + classificação textual 


###### Work in progress

## Objetivo

O objetivo deste repositório é desenvolver um app capaz de captar vagas do linkedin a partir de uma pesquisa, armazena-las em um csv, e diariamente ser rodado na nuvem (AWS). 
O algoritmo classificará as vagas encontradas através de machine learning - o modelo será desenvolvido em breve. 

## Sequencial de desenvolvimento
    1) Scrape inicial de vagas pela pesquisa por "vagas";
    2) Classificação manual das vagas encontradas, entre 0 e 2, onde:
        0 -> Vaga não relevante
        1 -> Vaga Relevante
        2 - Vaga muito relevante
    3) Treinar o modelo de classificação - Inicialmente utilizarei Naive-Bayes, XG-boost e Random Forests para classificação. 
    O modelo que performar melhor de acordo com as métricas será o selecionado;
    4)Desenvolver o scraper que será rodado diariamente na nuvem;
    5)Desenvolver template de e-mail HTML e o módulo que envia diariamente;
    6) Subir o código para uma instacia EC2, e programar a execução do código diariamente;
    7) Conseguir uma vaga como cientista de dados 😀
## Contribuição
Fique a vontade para contribuir neste projeto e usa-lo como desejar, com suas devidas adaptações.

# WebScraper de vagas de dados + Classificação textual com XGBoost

## Objetivo

Este projeto consiste em um aplicativo desenvolvido para automatizar a busca por vagas no campo de dados em grandes empresas, utilizando o LinkedIn como plataforma de pesquisa. A aplicação é capaz de captar vagas, classificá-las de acordo com a sua relevância utilizando Machine Learning, e então enviar um e-mail diariamente com as vagas mais relevantes.

O processo é executado na nuvem (AWS), permitindo uma busca e análise constantes sem a necessidade de interação manual constante.

## Funcionalidades

- **Web Scraping:** A aplicação raspa as vagas listadas no LinkedIn com base em uma consulta predefinida, armazenando os resultados em um arquivo CSV.

- **Classificação de Vagas:** Utilizando um modelo de Machine Learning treinado previamente (XGBoost), a aplicação classifica as vagas raspadas de acordo com a sua relevância.

- **Notificação por e-mail:** A aplicação envia diariamente um e-mail para o usuário com as vagas mais relevantes encontradas.

## Sequencial de desenvolvimento

1) Realização do scraping inicial de vagas pela pesquisa por "("(data science)" OR "cientista de dados)" OR "machine learning")"; 
2) Classificação manual das vagas encontradas, entre 0 e 2, onde:
    - 0: Vaga não relevante
    - 1: Vaga Relevante
    - 2: Vaga muito relevante
3) Treinamento do modelo de classificação: Manualmente fiz o label de todas as vagas encontradas (400+), depois foi treinado um modelo XGBoost para classificação baseado nas minhas labels.
4) Desenvolvimento do scraper a ser executado diariamente na nuvem;
5) Desenvolvimento do template de e-mail HTML e do módulo que envia e-mails diariamente;
6) Subida do código para uma instância EC2, programando a execução do código diariamente;
7) Obtenção de uma vaga como cientista de dados como resultado final! 🎉

## Contribuição

Sinta-se à vontade para contribuir para este projeto e usá-lo como desejar, com as devidas adaptações. Seu feedback e contribuições são muito apreciados.

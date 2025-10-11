# Football Analytics API & CLI

## Visão Geral

Este projeto é uma aplicação de análise de dados de futebol que oferece tanto uma API web quanto uma interface de linha de comando (CLI). Ele permite aos usuários consultar estatísticas de times, confrontos diretos (H2H) e dados gerais de ligas como o Brasileirão e a Premier League. Além disso, inclui uma ferramenta para calcular a probabilidade de eventos e odds justas com base em médias estatísticas.


## Descrição dos Arquivos

### Raiz do Projeto

-   **`config.py`**
    -   Centraliza as configurações do projeto.
    -   Define dicionários como `LEAGUE_CONFIG` que contêm informações essenciais para cada liga, como URLs para verificação de atualizações, URLs para download de CSVs e os caminhos onde os arquivos de dados são salvos.

### Diretório `api/`

-   **`main.py`**
    -   É o ponto de entrada da aplicação FastAPI.
    -   Inicializa a instância do FastAPI e inclui os roteadores para cada liga (Brasileirão e Premier League), que são criados pela `router_factory`.
    -   Define uma rota raiz (`/`) para uma mensagem de boas-vindas.

-   **`router_factory.py`**
    -   Responsável por criar e configurar os roteadores da API de forma dinâmica.
    -   A função `create_league_router` gera um `APIRouter` com endpoints padronizados para uma determinada liga (`/teams`, `/teams/{team}/{stat}`, `/h2h/{team1}/{team2}`, etc.).
    -   Essa abordagem evita a repetição de código, já que as rotas para a Premier League e o Brasileirão são funcionalmente idênticas.

-   **`dependencies.py`**
    -   Gerencia as dependências da API usando o sistema de injeção de dependências do FastAPI.
    -   As funções `get_brasileirao` e `get_premier_league` carregam os dados de seus respectivos CSVs e retornam uma instância das classes `Brasileirao` ou `Premier`.
    -   Isso permite que os dados sejam "injetados" nos endpoints, facilitando os testes e o gerenciamento de dados.

### Diretório `model/`

-   **`league.py`**
    -   Define a classe base `League`, que serve como um modelo genérico para qualquer liga de futebol.
    -   Implementa métodos comuns para manipulação de dados, como filtrar por time (`by_team`), obter confrontos diretos (`head_to_head`), calcular médias e somas de estatísticas, e obter um resumo de resultados (vitórias, derrotas, empates).

-   **`brasileirao.py`**
    -   Define a classe `Brasileirao`, que herda de `League`.
    -   É especializada para o conjunto de dados do Brasileirão, mapeando as colunas de gols (`HG`, `AG`) e adicionando funcionalidades específicas, como o método `by_year` para filtrar partidas por temporada.

-   **`premier.py`**
    -   Define a classe `Premier`, que também herda de `League`.
    -   É especializada para o conjunto de dados da Premier League, que é mais rico em estatísticas.
    -   Mapeia uma grande variedade de estatísticas (gols, chutes, escanteios, faltas, cartões) e implementa métodos específicos, como `goals_second_half_sum` e `total_cards_sum`, que não se aplicam a outras ligas.

### Diretório `services/`

-   **`api_handlers.py`**
    -   Contém a lógica de negócio que é executada pelos endpoints da API.
    -   Funções como `handle_team`, `handle_h2h` e `handle_league` recebem a instância da liga e os parâmetros da requisição, utilizam os métodos da classe `League` para processar os dados e retornam uma resposta formatada junto com um código de status HTTP.
    -   Também integra o `odd_calculator` para fornecer análises de probabilidade diretamente na API.

-   **`cli_handlers.py`**
    -   Contém a lógica de negócio para a interface de linha de comando (CLI).
    -   As funções aqui são projetadas para interagir com o usuário, recebendo entradas (`input`) e exibindo resultados (`print`).
    -   `handle_team`, `handle_h2h`, e `handle_league` guiam o usuário através de menus para selecionar times, estatísticas e filtros.

-   **`data_loader.py`**
    -   Responsável por carregar e pré-processar os dados dos arquivos CSV.
    -   As funções `load_brasileirao` e `load_premier_25_26` leem os CSVs, selecionam as colunas relevantes, renomeiam colunas para um padrão consistente (`Home`, `Away`, `FTR`) e definem a data como índice do DataFrame.
    -   Isso garante que as classes do `model` recebam DataFrames limpos e padronizados.

-   **`odd_calculator.py`**
    -   Um módulo de serviço puramente matemático.
    -   Utiliza a distribuição de Poisson (`scipy.stats.poisson`) para calcular a probabilidade de um evento ocorrer com base em uma média.
    -   Inclui funções para converter probabilidade em "odd justa" (`calculate_odd`) e para calcular a margem de lucro de uma casa de apostas (`calculate_house_edge`).

-   **`dataset_updater.py`**
    -   Um serviço utilitário para manter os dados das ligas atualizados.
    -   Ele verifica a data da última atualização de um arquivo de dados local e a compara com a data de atualização no site `football-data.co.uk`.
    -   Se uma atualização estiver disponível (`is_updated`), ele baixa o novo arquivo CSV (`download_csv`).

---

## Endpoints da API

A API é estruturada com um prefixo por liga (`/premier` para a Premier League e `/brasileirao` para o Campeonato Brasileiro).

Substitua `{prefixo}` por `premier` ou `brasileirao`.

### 1. Listar todos os times

-   **Rota**: `GET /{prefixo}/teams`
-   **Descrição**: Retorna uma lista com todos os times disponíveis no dataset da liga.
-   **Exemplo de Uso**: `http://127.0.0.1:8000/premier/teams`
-   **Resposta de Sucesso (200 OK)**:
    ```json
    {
      "teams": ["Arsenal", "Man City", "Liverpool", "..."]
    }
    ```

### 2. Obter estatísticas de um time

-   **Rota**: `GET /{prefixo}/teams/{team}/{stat}`
-   **Descrição**: Retorna a soma total e a média por jogo de uma estatística específica para um time. Opcionalmente, pode calcular odds com base na média.
-   **Parâmetros de Rota**:
    -   `team` (string): Nome do time.
    -   `stat` (string): Estatística desejada (ex: `goals`, `shots`, `corners`).
-   **Parâmetros de Query**:
    -   `threshold` (float): Limiar para o cálculo de probabilidade (ex: 2.5 para gols).
    -   `mode` (string): Modo do cálculo: `over`, `under` ou `exactly`.
    -   `house_odd` (float): Odd da casa de apostas para calcular o *house edge*.
-   **Exemplo de Uso (Simples)**: `http://127.0.0.1:8000/premier/teams/Arsenal/goals`
-   **Resposta de Sucesso (200 OK)**:
    ```json
    {
      "per game": 2.45,
      "sum": 93
    }
    ```
-   **Exemplo de Uso (com Calculadora de Odds)**: `http://127.0.0.1:8000/premier/teams/Arsenal/goals?threshold=2.5&mode=over&house_odd=1.85`
-   **Resposta de Sucesso (200 OK)**:
    ```json
    {
        "per game": 2.45,
        "sum": 93,
        "odd": {
            "probability_percent": 44.47,
            "fair_odd": 2.25,
            "house_edge_percent": 21.61
        }
    }
    ```

### 3. Obter resumo de confronto direto (H2H)

-   **Rota**: `GET /{prefixo}/h2h/{team1}/{team2}`
-   **Descrição**: Retorna um resumo de vitórias, derrotas e empates em confrontos diretos entre dois times.
-   **Parâmetros de Rota**:
    -   `team1` (string): Nome do primeiro time.
    -   `team2` (string): Nome do segundo time.
-   **Parâmetros de Query**:
    -   `only_home` (bool): Se `true`, retorna apenas os jogos com `team1` como mandante.
    -   `year_start` (int): Ano de início do filtro (específico do Brasileirão).
    -   `year_end` (int): Ano de fim do filtro (específico do Brasileirão).
-   **Exemplo de Uso**: `http://127.0.0.1:8000/premier/h2h/Arsenal/Man Utd`
-   **Resposta de Sucesso (200 OK)**:
    ```json
    {
        "Arsenal": {
            "wins": 10,
            "losses": 15,
            "draws": 8
        },
        "Man Utd": {
            "wins": 15,
            "losses": 10,
            "draws": 8
        }
    }
    ```

### 4. Listar todas as estatísticas disponíveis

-   **Rota**: `GET /{prefixo}/stat`
-   **Descrição**: Retorna uma lista de todas as estatísticas disponíveis para consulta na liga.
-   **Exemplo de Uso**: `http://127.0.0.1:8000/premier/stat`
-   **Resposta de Sucesso (200 OK)**:
    ```json
    {
      "stats": [
        "goals",
        "ht_goals",
        "shots",
        "shots_on_target",
        "corners",
        "fouls",
        "yellow_cards",
        "red_cards",
        "cards",
        "second half goals"
      ]
    }
    ```

### 5. Obter estatísticas gerais da liga

-   **Rota**: `GET /{prefixo}/league/{stat}`
-   **Descrição**: Retorna a soma total e a média por jogo de uma estatística para toda a liga.
-   **Parâmetros de Rota**:
    -   `stat` (string): Estatística desejada (ex: `goals`).
-   **Parâmetros de Query**:
    -   `start_year` (int): Ano de início do filtro (específico do Brasileirão).
    -   `end_year` (int): Ano de fim do filtro (específico do Brasileirão).
-   **Exemplo de Uso**: `http://127.0.0.1:8000/brasileirao/league/goals?start_year=2022&end_year=2023`
-   **Resposta de Sucesso (200 OK)**:
    ```json
    {
        "per_game": 2.51,
        "sum": 1898
    }
    ```

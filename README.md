# ⚙️ Offshore Predictive Maintenance System

Sistema educacional de manutenção preditiva para bombas centrífugas, desenvolvido para simular um pipeline de monitoramento industrial utilizando **Python, PostgreSQL, Machine Learning, FastAPI e Streamlit**.

O projeto simula dados de sensores de uma bomba centrífuga, armazena as leituras em banco de dados, identifica condições anormais por regras, utiliza Machine Learning para classificar o estado operacional do equipamento e disponibiliza os resultados através de uma API e de um dashboard.

> ⚠️ Este projeto utiliza dados e limites operacionais simulados para fins educacionais. Os resultados não representam parâmetros reais de equipamentos offshore.

---

## 🎯 Objetivo

Construir um sistema completo capaz de representar, de forma educacional, o fluxo de uma aplicação de manutenção preditiva:

```text
Sensores simulados
        ↓
Geração de telemetria
        ↓
PostgreSQL
        ↓
Detecção de anomalias
        ↓
Geração de alertas
        ↓
Machine Learning
        ↓
FastAPI
        ↓
Dashboard Streamlit
```

O projeto foi desenvolvido com foco no aprendizado de:

- Python
- Banco de dados relacional
- SQL
- Análise de dados
- Machine Learning
- APIs REST
- Visualização de dados
- Organização e arquitetura de projetos

---

## 🧠 Machine Learning

O sistema utiliza um modelo **Random Forest Classifier** para classificar o estado da bomba em três categorias:

- `NORMAL`
- `DEGRADACAO`
- `FALHA`

As features utilizadas pelo modelo são:

```text
temperatura_celsius
vibracao_mm_s
pressao_bar
```

Os dados utilizados no treinamento são gerados pelo próprio simulador do projeto.

### Dataset

Foram gerados:

```text
20 ciclos operacionais
30 leituras por ciclo
600 leituras no total
```

Cada ciclo representa uma progressão simulada:

```text
NORMAL → DEGRADACAO → FALHA
```

O identificador `ciclo_id` permite manter leituras pertencentes ao mesmo ciclo agrupadas durante a avaliação do modelo.

---

## 📊 Avaliação do modelo

Inicialmente, o modelo foi avaliado utilizando uma separação fixa de ciclos:

```text
16 ciclos → treinamento
4 ciclos  → teste
```

Resultado:

```text
Treinamento: 480 amostras
Teste: 120 amostras

Acurácia: 90,83%
```

Também foi utilizada validação cruzada com **GroupKFold**, mantendo ciclos completos separados entre treinamento e teste.

Resultados dos 5 folds:

| Fold | Acurácia |
|------|----------|
| 1 | 95,83% |
| 2 | 89,17% |
| 3 | 94,17% |
| 4 | 95,00% |
| 5 | 93,33% |

**Acurácia média: 93,50%**

Após a avaliação, o modelo final foi treinado utilizando as **600 leituras disponíveis**.

> As métricas representam desempenho sobre dados sintéticos gerados pelo simulador e não devem ser interpretadas como desempenho em equipamentos industriais reais.

---

## 🚨 Detecção de anomalias

Além do Machine Learning, o sistema possui uma camada de detecção baseada em regras.

Os limites utilizados na simulação são:

| Sensor | Condição de alerta |
|--------|--------------------|
| Temperatura | > 80 °C |
| Vibração | > 6 mm/s |
| Pressão | < 15 bar |

Quando uma leitura ultrapassa um desses limites, um alerta pode ser registrado no banco de dados.

Esses valores são parâmetros educacionais definidos exclusivamente para a simulação.

---

## 🗄️ Banco de dados

O projeto utiliza **PostgreSQL**.

Principais tabelas:

### `equipamentos`

Armazena informações sobre os equipamentos monitorados.

### `sensores_telemetria`

Armazena as leituras dos sensores:

- temperatura;
- vibração;
- pressão;
- timestamp;
- status;
- estado simulado;
- ciclo operacional.

### `alertas`

Armazena anomalias identificadas pelo sistema de regras.

### `manutencoes`

Estrutura preparada para armazenar registros de manutenção dos equipamentos.

---

## 🌐 API

A aplicação possui uma API desenvolvida com **FastAPI**.

Principais endpoints:

```text
GET /equipamentos
GET /sensores
GET /alertas
GET /previsao
```

A documentação interativa pode ser acessada através do Swagger disponibilizado automaticamente pelo FastAPI em:

```text
/docs
```

---

## 📈 Dashboard

O dashboard foi desenvolvido utilizando **Streamlit**.

Ele apresenta:

- temperatura atual;
- vibração atual;
- pressão atual;
- resultado da detecção baseada em regras;
- classificação realizada pelo Machine Learning;
- probabilidades de cada estado;
- histórico dos sensores;
- últimas leituras;
- alertas recentes;
- informações sobre o modelo.

O dashboard permite comparar a abordagem tradicional baseada em regras com a classificação realizada pelo modelo de Machine Learning.

---

## 🏗️ Estrutura do projeto

```text
offshore-predictive-maintenance/
│
├── analysis/
│   ├── exploratory_analysis.py
│   └── anomaly_detection.py
│
├── api/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── equipment.py
│       ├── sensors.py
│       ├── alerts.py
│       └── prediction.py
│
├── dashboard/
│   └── app.py
│
├── database/
│   ├── schema.sql
│   └── queries.sql
│
├── docs/
│   ├── relatorio-projeto.md
│   ├── arquitetura.md
│   └── banco-de-dados.md
│
├── ml/
│   ├── generate_dataset.py
│   ├── train.py
│   ├── predict.py
│   └── model/
│       └── random_forest.pkl
│
├── simulator/
│   ├── sensor_generator.py
│   └── save_reading.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠️ Tecnologias utilizadas

- Python
- PostgreSQL
- SQLAlchemy
- Pandas
- NumPy
- Scikit-learn
- FastAPI
- Uvicorn
- Streamlit
- Matplotlib
- Git
- GitHub

---

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
cd offshore-predictive-maintenance
```

### 2. Crie o ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`.

Exemplo:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=offshore_maintenance
DATABASE_USER=postgres
DATABASE_PASSWORD=sua_senha
```

### 6. Configure o PostgreSQL

Execute:

```text
database/schema.sql
```

para criar as tabelas necessárias.

### 7. Treine o modelo

```bash
python -m ml.train
```

### 8. Execute a API

```bash
uvicorn api.main:app --reload
```

### 9. Execute o dashboard

Em outro terminal:

```bash
streamlit run dashboard/app.py
```

---

## 🔐 Segurança

Credenciais do banco de dados são armazenadas em um arquivo `.env`, que não deve ser enviado ao GitHub.

O repositório contém apenas o `.env.example` como referência de configuração.

---

## 📌 Limitações

Este projeto é uma simulação educacional.

Os dados dos sensores são sintéticos e os limites utilizados na detecção de anomalias não representam especificações técnicas de bombas centrífugas reais.

O modelo de Machine Learning foi treinado e avaliado exclusivamente utilizando os dados gerados pelo simulador.

Portanto, o sistema não deve ser utilizado para decisões de manutenção em equipamentos reais.

---

## 🚀 Possíveis evoluções

- criação de features temporais;
- médias móveis dos sensores;
- análise da tendência de degradação;
- previsão de tempo até falha;
- múltiplos equipamentos;
- histórico de manutenção;
- testes automatizados;
- containerização com Docker;
- deploy da API e dashboard;
- integração da interface diretamente com a API.

---

## 👨‍💻 Autor

Desenvolvido como projeto de portfólio e estudo de desenvolvimento de software, análise de dados e Machine Learning.
# Python WhatsApp Serviço de Automação

Este projeto é uma ferramenta de automação backend desenvolvida em Python, projetada para integrar fluxos de dados de um banco PostgreSQL (Supabase) com a API do WhatsApp (Z-API).

A solução permite a leitura automática de contatos cadastrados e o disparo de mensagens personalizadas de forma eficiente e escalável.

## Tecnologias

* **Python 3**
* **Supabase** (PostgreSQL)
* **Z-API** (Gateway de mensagens)
* **Requests** (Requisições HTTP)
* **Python-dotenv** (Gestão de variáveis de ambiente)

## Funcionalidades

- **Integração de Banco de Dados:** Conexão segura e consulta de contatos via client oficial do Supabase.
- **Automação de Mensagens:** Disparo em lote via REST API.
- **Tratamento de Logs:** Monitoramento de status de execução (sucesso/erro) com persistência em arquivo local (`automacao.log`).
- **Segurança:** Gestão de credenciais através de variáveis de ambiente (`.env`).

## Como utilizar

### 1. Clonar o Repositório
```bash
git clone https://github.com/Emanuel-repository/integracao-supabase-zapi
cd integracao-supabase-zapi
```

### 2. Configurar o Ambiente Virtual (Recomendado)
```bash
python -m venv venv
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate     # No Windows
```

### 3. Instalar as Dependências
Instale as bibliotecas necessárias listadas no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as suas credenciais do Supabase e da Z-API:
```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_anon_public
ZAPI_INSTANCE=seu_id_da_instancia
ZAPI_TOKEN=seu_token_da_instancia
ZAPI_CLIENT_TOKEN=seu_client_token_se_houver
```

### 5. Executar a Aplicação
Rode o script principal para iniciar a leitura do banco e o disparo das mensagens:
```bash
python main.py
```

*Os eventos e o status de cada envio serão exibidos no terminal e salvos automaticamente no arquivo `automacao.log`.*

## Licença
Este projeto é open-source sob a licença MIT. Sinta-se à vontade para utilizar e estender a solução.
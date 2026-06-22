# Desafio Técnico - Integração Supabase e Z-API

Script em Python que lê contatos armazenados em um banco de dados no Supabase e realiza o disparo de mensagens automáticas via WhatsApp utilizando a Z-API.

## Tecnologias Utilizadas

* Python 3
* Supabase (Banco de Dados Postgres)
* Z-API (Disparo de Mensagens)
* `requests`, `python-dotenv`, `supabase`

## Setup da Tabela (Supabase)

Crie uma tabela no Supabase chamada `contatos` contendo as seguintes colunas:

* `id` (int8 ou uuid, Primary Key)
* `nome` (text)
* `telefone` (text) -> *Formato esperado: DDI + DDD + Número (ex: 5511999999999)*

## Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SUPABASE_URL=url_do_supabase
SUPABASE_KEY=chave_anon_do_supabase
ZAPI_INSTANCE=id_da_instancia_zapi
ZAPI_TOKEN=token_zapi
ZAPI_CLIENT_TOKEN=client_token_zapi_se_houver

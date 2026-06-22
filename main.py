import os
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automacao.log", encoding="utf-8"), # Salva no arquivo automacao.log
        logging.StreamHandler()
    ]
)

def carregar_variaveis_ambiente():
    """Carrega e valida as variáveis do arquivo .env"""
    load_dotenv()
    env_vars = {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
        "ZAPI_INSTANCE": os.getenv("ZAPI_INSTANCE"),
        "ZAPI_TOKEN": os.getenv("ZAPI_TOKEN"),
        "ZAPI_CLIENT_TOKEN": os.getenv("ZAPI_CLIENT_TOKEN", "")
    }
    
    # Verifica se variáveis cruciais estão faltando
    missing_vars = [key for key, val in env_vars.items() if not val and key != "ZAPI_CLIENT_TOKEN"]
    if missing_vars:
        logging.error(f"Variáveis de ambiente ausentes: {', '.join(missing_vars)}")
        raise EnvironmentError("Configure o arquivo .env corretamente.")
        
    return env_vars

def buscar_contatos(supabase_url: str, supabase_key: str):
    """Busca os contatos cadastrados na tabela 'contatos' no Supabase"""
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        # Seleciona todos os contatos
        response = supabase.table('contatos').select("*").execute()
        
        if not response.data:
            logging.warning("Nenhum contato encontrado no Supabase.")
            return []
            
        return response.data
    except Exception as e:
        logging.error(f"Erro ao buscar contatos no Supabase: {e}")
        return []

def enviar_mensagem(nome: str, telefone: str, instance: str, token: str, client_token: str):
    """Envia a mensagem via Z-API para o contato especificado"""
    mensagem = f"Olá, {nome} tudo bem com você?"
    
    # Endpoint de envio do Z-API
    url = f"https://api.z-api.io/instances/{instance}/token/{token}/send-text"
    
    headers = {
        "Content-Type": "application/json"
    }
    if client_token:
        headers["Client-Token"] = client_token
        
    payload = {
        "phone": telefone,
        "message": mensagem
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Dispara exceção para códigos de erro HTTP
        logging.info(f"Mensagem enviada com sucesso para {nome} ({telefone}).")
    except requests.exceptions.RequestException as e:
        logging.error(f"Falha ao enviar mensagem para {nome} ({telefone}). Erro: {e}")

def main():
    logging.info("Iniciando o script de integração Supabase + Z-API...")
    
    try:
        # 1. Carrega o ambiente
        env = carregar_variaveis_ambiente()
        
        # 2. Busca os dados no banco
        contatos = buscar_contatos(env["SUPABASE_URL"], env["SUPABASE_KEY"])
        
        # 3. Processa e envia as mensagens
        for contato in contatos[:3]: # limite de três pessoas, no supabase inseri meu proprio numero mas caso ouvessem mais não ultrapassaria 3 envios
            nome = contato.get('nome')
            telefone = contato.get('telefone')
            
            if nome and telefone:
                enviar_mensagem(
                    nome=nome,
                    telefone=telefone,
                    instance=env["ZAPI_INSTANCE"],
                    token=env["ZAPI_TOKEN"],
                    client_token=env["ZAPI_CLIENT_TOKEN"]
                )
            else:
                logging.warning(f"Contato ignorado (dados incompletos): {contato}")
                
        logging.info("Processo finalizado com sucesso.")
        
    except Exception as e:
        logging.critical(f"Execução interrompida devido a um erro crítico: {e}")

if __name__ == "__main__":
    main()
import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

def carregar_variaveis_ambiente():
    load_dotenv()
    env_vars = {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
        "ZAPI_INSTANCE": os.getenv("ZAPI_INSTANCE"),
        "ZAPI_TOKEN": os.getenv("ZAPI_TOKEN"),
        "ZAPI_CLIENT_TOKEN": os.getenv("ZAPI_CLIENT_TOKEN", "")
    }
    
    missing_vars = [key for key, val in env_vars.items() if not val and key != "ZAPI_CLIENT_TOKEN"]
    if missing_vars:
        print(f"Variáveis de ambiente ausentes: {', '.join(missing_vars)}")
        raise EnvironmentError("Configure o arquivo .env corretamente.")
        
    return env_vars

def buscar_contatos(supabase_url: str, supabase_key: str):
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        response = supabase.table('contatos').select("*").execute()
        
        if not response.data:
            print("Nenhum contato encontrado no Supabase.")
            return []
            
        return response.data
    except Exception as e:
        print(f"Erro ao buscar contatos no Supabase: {e}")
        return []

def enviar_mensagem(nome: str, telefone: str, instance: str, token: str, client_token: str):
    mensagem = f"Olá, {nome} tudo bem com você?"
    
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
        print(f"Mensagem enviada com sucesso para {nome} ({telefone}).")
    except requests.exceptions.RequestException as e:
        print(f"Falha ao enviar mensagem para {nome} ({telefone}). Erro: {e}")

def main():
    print("Iniciando o script de integração Supabase + Z-API...")
    
    try:
        env = carregar_variaveis_ambiente()
        
        contatos = buscar_contatos(env["SUPABASE_URL"], env["SUPABASE_KEY"])
        
        for contato in contatos[:3]:
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
                print(f"Contato ignorado (dados incompletos): {contato}")
                
        print("Processo finalizado com sucesso.")
        
    except Exception as e:
        print(f"Execução interrompida devido a um erro crítico: {e}")

if __name__ == "__main__":
    main()
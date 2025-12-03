def print_setup_instructions():
    print("\n" + "="*60)
    print("CONFIGURAÇÃO DO WHATSAPP (EVOLUTION API)")
    print("="*60)
    
    print("\n[1] PRÉ-REQUISITOS:")
    print("    - Docker Desktop instalado e rodando.")
    print("    - Docker Compose instalado.")
    
    print("\n[2] COMO INICIAR:")
    print("    Abra um terminal na raiz do projeto e execute:")
    print("    > docker-compose up -d")
    
    print("\n[3] PRÓXIMOS PASSOS:")
    print("    1. Aguarde uns 30 segundos para o container iniciar.")
    print("    2. Acesse no navegador: http://localhost:8080/manager")
    print("    3. Use a API Key configurada no docker-compose.yml:")
    print("       Key: 429683C4C977415CAAFCCE10F7D57E11")
    print("    4. Crie uma instância chamada 'chatbot' e leia o QR Code.")
    
    print("\n[4] CONECTAR AO CHATBOT:")
    print("    No painel da Evolution API, configure o Webhook da instância:")
    print("    - URL: http://host.docker.internal:8000/webhook")
    print("    - Events: MESSAGES_UPSERT")
    print("    - Habilitar: Sim")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print_setup_instructions()

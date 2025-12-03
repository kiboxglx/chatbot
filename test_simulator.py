import requests
import json
import time

BASE_URL = "http://localhost:8000/webhook"

def enviar_mensagem(telefone, texto, cenario):
    print(f"\n{'='*50}")
    print(f"{cenario}")
    print(f"{'='*50}")
    print(f"Enviando de: {telefone}")
    print(f"Mensagem: {texto}")
    
    payload = {
        "remoteJid": telefone,
        "conversation": texto
    }
    
    try:
        start_time = time.time()
        response = requests.post(BASE_URL, json=payload)
        duration = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Tempo: {duration:.2f}s")
        
        try:
            data = response.json()
            output = f"CENÁRIO: {cenario}\nSTATUS: {response.status_code}\nJSON: {json.dumps(data, indent=2, ensure_ascii=False)}\n{'-'*50}\n"
            print(output)
            with open("test_results.txt", "a", encoding="utf-8") as f:
                f.write(output)
        except json.JSONDecodeError:
            print("Resposta não é JSON válido.")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("ERRO: Não foi possível conectar ao servidor. Verifique se o uvicorn está rodando em http://localhost:8000")

if __name__ == "__main__":
    # Aguarda um pouco para garantir que o usuário leia
    print("Iniciando simulador de testes do WhatsApp...")
    
    # CENÁRIO 1: Cliente Desconhecido
    enviar_mensagem(
        telefone="5511000000000",
        texto="Quero meu boleto",
        cenario="CENÁRIO 1: Cliente Desconhecido"
    )

    # CENÁRIO 2: Cliente Cadastrado pedindo Boleto
    enviar_mensagem(
        telefone="5511999999999",
        texto="Preciso da segunda via do DAS",
        cenario="CENÁRIO 2: Pedido de Boleto (Cliente OK)"
    )

    # CENÁRIO 3: Cliente Cadastrado querendo Humano
    enviar_mensagem(
        telefone="5511999999999",
        texto="Quero falar com um atendente, estou com problema",
        cenario="CENÁRIO 3: Falar com Humano (Cliente OK)"
    )

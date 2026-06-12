import os
import ssl
import json
import time
import random
from xmlrpc import client
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from dotenv import load_dotenv

load_dotenv()

# Configurações do HiveMQ Cloud
broker_url = os.getenv("HIVEMQ_HOST")
broker_port = int(os.getenv("HIVEMQ_PORT", 8883))
broker_user = os.getenv("HIVEMQ_USER")
broker_pass = os.getenv("HIVEMQ_PASSWORD")

TOPICO_NOVO_JOGADOR = "pokemon/jogadores/criado"
TOPICO_TROCA = "pokemon/trocas/solicitada"

def _publicar_no_mqtt(topico, dados):
    meu_id_unico = f"Pokemon_API_Produtor_{random.randint(1000, 9999)}"
    
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id=meu_id_unico)
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.username_pw_set(broker_user, broker_pass)
    
    try:
        client.connect(broker_url, broker_port, 60)
        
        client.loop_start()
        
        payload = json.dumps(dados)
        
        mensagem_info = client.publish(topico, payload)
        
        mensagem_info.wait_for_publish()
        
        client.disconnect()
        client.loop_stop()
        
    except Exception as e:
        print(f"❌ Erro MQTT: Não foi possível publicar no tópico {topico}. Erro: {e}")

def criar_jogador(id_jogador: int):
    print(f"🎮 API solicitou a criação do jogador: {id_jogador}")
    dados = {"id_jogador": int(id_jogador)}
    _publicar_no_mqtt(TOPICO_NOVO_JOGADOR, dados)
    print(f"✅ SUCESSO! Evento do jogador {id_jogador} disparado!")

def simular_troca(origem: int, destino: int, enviados: list, recebidos: list):
    print(f"🔄 API solicitou troca: Jogador {origem} envia para {destino}")
    
    dados = {
        "jogador_origem": origem,
        "jogador_destino": destino,
        "cartas_enviadas": enviados,
        "cartas_recebidas": recebidos
    }
    
    _publicar_no_mqtt(TOPICO_TROCA, dados)
    print(f"✅ SUCESSO! Evento de troca disparado!")

if __name__ == "__main__":
    print("🛠️ --- MODO DE TESTE MANUAL DO PRODUTOR --- 🛠️")
    print("1 - Forçar criação de Novo Jogador")
    print("2 - Forçar Simulação de Troca")
    
    escolha = input("\nEscolha o teste que deseja forçar (1 ou 2): ")
    
    if escolha == "1":
        id_jog = input("Digite o ID do jogador: ")
        criar_jogador(int(id_jog))
        
    elif escolha == "2":
        origem = int(input("ID do Jogador Origem: "))
        destino = int(input("ID do Jogador Destino: "))
        
        env_input = input("IDs das cartas enviadas (ex: 1,2,3): ")
        rec_input = input("IDs das cartas recebidas (ex: 4,5): ")
        
        enviadas = [int(x.strip()) for x in env_input.split(',') if x.strip()]
        recebidas = [int(x.strip()) for x in rec_input.split(',') if x.strip()]
        
        simular_troca(origem, destino, enviadas, recebidas)
        
    else:
        print("❌ Opção inválida.")
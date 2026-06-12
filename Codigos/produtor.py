import os
import ssl
import json
import time
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

def criar_jogador():
    print("🎮 --- CRIADOR DE JOGADORES --- 🎮")
    id_jogador = input("Digite o ID para o novo jogador: ")
    
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="Pokemon_Produtor_Local")
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.username_pw_set(broker_user, broker_pass)
    
    try:
        print("🌐 Conectando à nuvem...")
        client.connect(broker_url, broker_port, 60)
        payload = id_jogador 
        
        client.publish(TOPICO_NOVO_JOGADOR, payload)
        print(f"✅ SUCESSO! Evento de criação do jogador {id_jogador} disparado para a nuvem!")
        
        time.sleep(2)
        
        client.disconnect()
    except Exception as e:
        print(f"❌ Erro ao conectar ou enviar: {e}")

if __name__ == "__main__":
    criar_jogador()
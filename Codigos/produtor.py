import os
import ssl
import json
import time
import random
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
        
        payload = json.dumps(dados)
        client.publish(topico, payload)
        
        time.sleep(1.5)
        client.disconnect()
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
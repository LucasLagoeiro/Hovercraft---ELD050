# O codigo completo do ESP eh apresentado a seguir comentado
# Ele esta dividido em blocos identificados para facilitar o seu entendimento

# Antes de enviar o código, use Ctrl+C no shell para garantir que o ESP
# não esteja executando o codigo e aguarde ate que apareca o simbolo ">>"
# no shell.
# Apos carregar o codigo, clique no botao "EN" do ESP.

#===============================================================
# Bibliotecas
#===============================================================

from machine import Pin, PWM
import network
import time
from time import sleep
from umqtt.robust import MQTTClient # necessaria para a comunicacao com o servidor MQTT
import sys
import json
from fsm import FSM_Robot #Finite State Machine for the robot

#===============================================================
# Wi-Fi e Node-Red
#===============================================================

# Modifique os dados abaixo para a rede WiFi que o ESP deve se conectar
WIFI_SSID     = 'llagoeiro'
WIFI_PASSWORD = 'makerobot'

mqtt_client_id = bytes('cliente_'+'robot', 'utf-8') # um ID de cliente aleatorio

# Altere a variavel para o endereco IP do seu Raspberry Pi, de forma que
# ele se conecte ao broker MQTT
MQTT_IO_URL = '10.42.0.1'

# Caso o servidor MQTT exija usuario e senha
# MQTT_USERNAME   = 'usuario'
# MQTT_IO_KEY     = 'senha'


#===============================================================
# Leds, botao e variaveis
#===============================================================

# Pinos a utilizar para os LEDs com o ESP32
# robot = Motor(19,18,21)
# g = PWM(Pin(18), freq=20000, duty = 0)
# r = PWM(Pin(19), freq=20000, duty = 0)
# y = PWM(Pin(21), freq=20000, duty = 0)


# Guarda a informacao se alguem tocou a campainha
campainha = False

# Contador de tempo para a campainha
ini_tempo = 0

#===============================================================
# Conecta o ESP ao roteador, nao alterar
#===============================================================

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('Conectando...')
        timeout = 0
        while (not wifi.isconnected() and timeout < 10):
            print(10 - timeout)
            timeout = timeout + 1
            time.sleep(1) 
    if(wifi.isconnected()):
        print('Conectado')
    else:
        print('Nao conectado')
        sys.exit()

# Conecta ao roteador WiFi
connect_wifi()

# Caso o servidor MQTT nao exija usuario e senha
client = MQTTClient(client_id=mqtt_client_id, 
                    server=MQTT_IO_URL)

# Caso o servidor MQTT exija usuario e senha
# client = MQTTClient(client_id=mqtt_client_id, 
#                     server=MQTT_IO_URL, 
#                     user=MQTT_USERNAME, 
#                     password=MQTT_IO_KEY,
#                     ssl=False)

# Conecta ao cliente
try:
    client.connect()
except Exception as e:
    print('Nao foi possivel conectar ao servidor MQTT {}{}'.format(type(e).__name__, e))
    sys.exit()


#===============================================================
# Funcao callback
# Esta funcao eh executada quando algum dispositivo publica uma
# mensagem em um topico em que seu ESP esta inscrito.
# Altere a funcao abaixo para adicionar a logica ao seu programa,
# para que quando um dispositivo publicar uma mensagem em um
# topico que seu ESP esteja inscrito, voce possa executar uma funcao.
#===============================================================
# isRunning = False
# state = 0
finite_state_machine = FSM_Robot()
def cb(topic, msg):
    # print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))            
    if topic == b'esp32/cmd_vel':
        # print(msg.decode())
        twist = json.loads(msg.decode()) 
        print(twist)
        finite_state_machine.update(twist['start'],twist['stop'],twist['robot_vel'],twist['robot_yaw'])

        


        
        # if state == 0:
        #     print("Robot is turnoff")
            
        # if isRunning:
        #     print("Robot is running")
        #     if twist['start'] == 1:
        #         print("Will stop the robot")
        #         isRunning = False
        #         robot.stopRobot()

        # if twist['start'] == 1 and not isRunning:
        #     isRunning = True
        #     robot.startRobot()
            
                
                
        # print(isRunning)
            
        #y.value(1)
        # g.duty(twist['robot_vel'])
        # y.duty(twist['robot_vel'])
        #print('x={0}'.format(joy['button']))

        


#===============================================================
# Assinar ou assinar novamente um topico
# Voce pode se inscrever em mais tópicos (para controlar
# mais LEDs neste exemplo)
#===============================================================

# Funcao Callback
client.set_callback(cb)

# Inscricao nos topicos
client.subscribe(b'esp32/cmd_vel')


#===============================================================
# Sua funcao
#===============================================================

while True:
    try:
        #==================================
        # Wi-Fi - Funcao que verifica o recebimento de novas mensagens
        client.check_msg()
        #print("Verificando a mensagem...")
        #==================================
    except: # Caso a conexao for perdida
        client.disconnect()
        sys.exit()







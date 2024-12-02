from machine import Pin, SPI
from sx127x import SX127x
import socket 
import comunes as c

# Configuración del socket UDP
UDP_IP = "192.168.171.38"  # Dirección IP de tu Mac con SDR++
UDP_PORT = 12345
LORA = ()
frecuencia = 868E6
bandwidth = 125E3

# Configuración de LoRa
lora_config = {
    'spi': SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19)),
    'cs': Pin(5, Pin.OUT),
    'rst': Pin(14, Pin.OUT),
    'dio0': Pin(26, Pin.IN),
    'frequency': frecuencia,
    'bandwidth': bandwidth,
    'spreading_factor': 7,
    'coding_rate': 5,
}

class LoRaReceiver:
    def __init__(self):
        LORA = SX127x(lora_config)
        c.Log("Inicializando LoRa...")
        self.received_data = []

    def iniciar(): 
        # Inicialización del módulo LoRa
        LORA = SX127x(lora_config)
        LORA.set_mode_rx()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    def receive_packet(self):
        if self.lora.receiver_mode:
            packet = self.lora.receive()
            if packet:
                data = packet.decode('utf-8', 'ignore')
                self.received_data.append(data)
                print(f"Paquete recibido: {data}")
            return packet

    def get_received_packets(self):
        return self.received_data[-10:]

    def set_frequency(self, frequency):
        self.lora.set_frequency(frequency)
        print(f"Frecuencia configurada a {frequency} Hz")

    def set_bandwidth(self, bandwidth):
        self.lora.set_bandwidth(bandwidth)
        print(f"Ancho de banda configurado a {bandwidth} Hz")
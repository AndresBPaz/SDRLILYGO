from machine import Pin, SoftSPI, I2C, SPI
from lib.sx127x import SX127x
import socket 
import comunes as c

class LoRaReceiver: 
   

    def __init__(self):
        # Configuración del socket UDP
        self.UDP_IP = "192.168.68.38"  # Dirección IP de tu Mac con SDR++
        self.UDP_PORT = 5296
        self.LORA = ()
        self.frecuencia = 869525000
        self.bandwidth = 125E3
      
        # Configuración de pines de LoRa
        self.lora_pins = {
            'dio_0': 26,
            'ss': 18,       # Chip select
            'reset': 23,    # Reset
            'sck': 5,       # SCK
            'miso': 19,     # MISO
            'mosi': 27,     # MOSI
        }

        # Inicialización del bus SoftSPI para LoRa
        self.lora_spi = SoftSPI(
            baudrate=10000000, polarity=0, phase=0,
            bits=8, firstbit=SoftSPI.MSB,
            sck=Pin(self.lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
            mosi=Pin(self.lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
            miso=Pin(self.lora_pins['miso'], Pin.IN, Pin.PULL_UP),
        )

        self.lora_default = {
            'frequency': self.frecuencia,
            'frequency_offset':0,
            'tx_power_level': 14,
            'signal_bandwidth': self.bandwidth,
            'spreading_factor': 9,
            'coding_rate': 5,
            'preamble_length': 8,
            'implicitHeader': False,
            'sync_word': 0x12,
            'enable_CRC': True,
            'invert_IQ': False,
            'debug': False,
        }

        # Inicialización del módulo LoRa con los parámetros adecuados
        self.LORA = SX127x(self.lora_spi, pins=self.lora_pins, parameters=self.lora_default)
        c.Log("Inicializando LoRa...")
        self.received_data = []

    def getUDP_IP(self): 
        return self.UDP_IP
    
    def getUDP_PORT(self): 
        return self.UDP_PORT

    def iniciar(self): 
        # Inicialización del módulo LoRa 
        self.LORA.set_mode_rx()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    def receive_packet(self):
        try:
            if self.LORA.receivedPacket():  # Revisa si receiver_mode es accesible
                packet = self.LORA.receive()
                if packet:
                    data = packet.decode('utf-8', 'ignore')
                    self.received_data.append(data)
                    print(f"Paquete recibido: {data}")
                    payload = LORA.readPayload().decode()
                    rssi = LORA.packetRssi()
                    print("RX: {} | RSSI: {}".format(payload, rssi))
                return packet
        except Exception as e:
            print(f"Error al recibir paquete: {e}")


    def get_received_packets(self):
        return self.received_data[-10:]

    def set_frequency(self, frequency):
        self.LORA.set_frequency(frequency)
        print(f"Frecuencia configurada a {frequency} Hz")

    def set_bandwidth(self, bandwidth):
        self.LORA.set_bandwidth(bandwidth)
        print(f"Ancho de banda configurado a {bandwidth} Hz")
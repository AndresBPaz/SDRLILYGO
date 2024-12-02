import network as n
import time as t
import comunes as c

# Configuración Wi-Fi
SSID = "Razones para tomar cafe"         # Nombre de tu red Wi-Fi
PASSWORD = "contrasena123"  # Contraseña de tu red Wi-Fi
 
class WiFiManager: 
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.sta_if = n.WLAN(n.STA_IF)

    def conectar(self):  
        if not self.sta_if.isconnected():
            print(f"Conectando a la red {self.ssid}...")
            self.sta_if.active(True)
            self.sta_if.connect(self.ssid, self.password)
            while not self.sta_if.isconnected():
                pass
        c.Log(f"Conexión establecida: {self.getIP()}")
        return True  # Retorna la IP del ESP32

    def desconectar(self): 
        self.sta_if.active(False)

    def estado(self): 
        return self.sta_if.isconnected()
    
    def getIP(self): 
        return self.sta_if.ipconfig("addr4")[0]
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

    def conectar():
        wlan = n.WLAN(n.STA_IF)
        wlan.active(True)
        wlan.connect(SSID, PASSWORD)
        c.Log("Conectando al Wi-Fi...")
        while not wlan.isconnected():
            t.sleep(1)
            c.Log("Intentando conexión...")
        c.Log("Conexión establecida:", wlan.ifconfig())
        return wlan.ifconfig()[0]  # Retorna la IP del ESP32

    def desconectar():
        wlan = n.WLAN(n.STA_IF)
        wlan.active(False)

    def estado():
        wlan = n.WLAN(n.STA_IF)
        return wlan.isconnected()
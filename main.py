import webrlp as w
import comunes as c
from WiFiManager import WiFiManager as wf
from LoRaReceiver import LoRaReceiver as s
import uasyncio as asy 
from WebServer import WebServer as wsrv

# main 
def main():
    wifi = wf("Razones para tomar cafe", "contrasena123")
    is_connected = wifi.conectar()

    lr = s()
    
    if is_connected: 
        ip = wifi.getIP()
        c.Log(f"Enviando datos UDP a {lr.getUDP_IP()}:{lr.getUDP_PORT()} desde {ip}")

    if wifi.estado():
        # iniciar webrepl
        # w.iniciar()

        # Crear servidor WebSocket
        web_server = wsrv(lr)
        #asyncio.run(web_server.start())  # Iniciar el servidor
        
        async def lora_loop():
            while True:
                lr.receive_packet()
                await asy.sleep(1)

        loop = asy.get_event_loop()
        loop.create_task(web_server.start())
        loop.create_task(lora_loop())
        loop.run_forever()
    else:
        c.Log("No se pudo conectar a la red Wi-Fi")

if __name__ == "__main__":
    main()
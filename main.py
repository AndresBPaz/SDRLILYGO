import webrlp as w
import comunes as c
import WiFiManager as wf 
import LoRaReceiver as s
import uasyncio as asy 
import WebServer as wsrv

# main 
def main():
    wifi = wf("Razones para tomar cafe", "contrasena123")
    wifi.connect()
    
    c.Log(f"Enviando datos UDP a {s.UDP_IP}:{s.UDP_PORT} desde {ip}")

    if wf.estado():
        # iniciar webrepl
        w.iniciar()
        
        lora_receiver = s()
        web_server = wsrv(lora_receiver)

        async def lora_loop():
            while True:
                lora_receiver.receive_packet()
                await asy.sleep(1)

        loop = asy.get_event_loop()
        loop.create_task(web_server.start())
        loop.create_task(lora_loop())
        loop.run_forever()
    else:
        c.Log("No se pudo conectar a la red Wi-Fi")

if __name__ == "__main__":
    main()
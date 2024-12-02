import uasyncio as asyncio
from uasyncio.websocket.server import WSReader, WSWriter

class WebServer:
    def __init__(self, lora_receiver):
        self.lora_receiver = lora_receiver
        self.clients = []  # Almacena clientes WebSocket conectados

    async def websocket_handler(self, reader, writer):
        print("Cliente WebSocket conectado")
        self.clients.append(writer)

        try:
            while True:
                # Mantén el WebSocket abierto
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Cliente desconectado: {e}")
        finally:
            self.clients.remove(writer)
            await writer.aclose()

    async def broadcast_packets(self):
        while True:
            if self.clients:
                packets = self.lora_receiver.get_received_packets()
                for writer in self.clients:
                    try:
                        await writer.awrite(str(packets).replace("'", '"'))
                    except Exception as e:
                        print(f"Error al enviar datos: {e}")
            await asyncio.sleep(2)  # Ajusta el intervalo de actualización si es necesario

    async def start(self):
        # Servidor HTTP para archivos estáticos
        server = await asyncio.start_server(self.handle_client, "0.0.0.0", 80)

        # Servidor WebSocket
        ws_server = await asyncio.start_server(
            self.websocket_handler, "0.0.0.0", 81
        )

        print("Servidor corriendo en http://<IP-de-tu-placa>")
        async with server, ws_server:
            await asyncio.gather(server.serve_forever(), ws_server.serve_forever())

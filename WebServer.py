import uasyncio as asyncio
import usocket as socket
from machine import Pin
from WiFiManager import WiFiManager as wf
import ujson as json   

class WebServer:
    def __init__(self, lora_receiver):
        self.lora_receiver = lora_receiver
        self.clients = []  # Almacena sockets conectados

    async def websocket_handler(self, reader, writer):
        print("Cliente WebSocket conectado")
        self.clients.append(writer)

        try:
            while True:
                msg = await reader.readline()
                if msg:
                    msg = msg.decode('utf-8').strip()  # Decodificar y limpiar
                    print(f"Mensaje recibido: {msg}")

                    try:
                        data = json.loads(msg)  # Parsear el mensaje JSON
                        action = data.get("action")

                        if action == "configure":
                            frequency = data.get("frequency")
                            bandwidth = data.get("bandwidth")
                            print(f"Configurando LoRa: Frecuencia={frequency}, Ancho de Banda={bandwidth}")
                            # Lógica para configurar LoRa aquí
                            response = {"status": "success", "message": "Configuración aplicada"}
                        elif action == "start_scan":
                            print("Iniciando escaneo")
                            # Lógica para iniciar el escaneo aquí
                            response = {"status": "success", "message": "Escaneo iniciado"}
                        elif action == "stop_scan":
                            print("Deteniendo escaneo")
                            # Lógica para detener el escaneo aquí
                            response = {"status": "success", "message": "Escaneo detenido"}
                        else:
                            response = {"status": "error", "message": "Acción no reconocida"}

                    except Exception as e:
                        print(f"Error procesando mensaje: {e}")
                        response = {"status": "error", "message": "Error procesando mensaje"}

                    # Enviar respuesta al cliente
                    await writer.awrite(json.dumps(response) + "\n")
        except Exception as e:
            print(f"Cliente desconectado: {e}")
        finally:
            self.clients.remove(writer)
            await writer.aclose()


    async def broadcast_packets(self):
        while True:
            if self.clients:
                packets = self.lora_receiver.get_received_packets()
                for client_socket in self.clients:
                    try:
                        await self._send(client_socket, str(packets).replace("'", '"'))
                    except Exception as e:
                        print(f"Error al enviar datos: {e}")
                        self.clients.remove(client_socket)
                        client_socket.close()
            await asyncio.sleep(2)

    async def start(self):
        # Configuración del servidor
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 81))
        server_socket.listen(5)
        print("Servidor corriendo en WebSocket ws://<IP-de-tu-placa>:81")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexión aceptada desde {addr}")
            asyncio.create_task(self.websocket_handler(client_socket))

    async def _websocket_handshake(self, client_socket, request):
        # Extraer el WebSocket Key
        key = ""
        for line in request.decode().split("\r\n"):
            if line.startswith("Sec-WebSocket-Key:"):
                key = line.split(": ")[1].strip()

        # Responder con el handshake
        accept_key = self._generate_accept_key(key)
        handshake_response = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
        )
        client_socket.send(handshake_response.encode())

    def _generate_accept_key(self, key):
        import ubinascii
        import hashlib

        GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        accept = key + GUID
        sha1 = hashlib.sha1(accept.encode()).digest()
        return ubinascii.b2a_base64(sha1).strip().decode()

    async def _recv(self, client_socket):
        try:
            return client_socket.recv(1024)
        except Exception as e:
            print(f"Error al recibir datos: {e}")
            return b""

    async def _send(self, client_socket, data):
        try:
            # Construir un marco de texto para WebSocket
            frame = bytearray()
            frame.append(0x81)  # 0x81 = texto y fin del mensaje
            length = len(data)
            if length <= 125:
                frame.append(length)
            elif length <= 65535:
                frame.append(126)
                frame.extend(length.to_bytes(2, 'big'))
            else:
                frame.append(127)
                frame.extend(length.to_bytes(8, 'big'))
            frame.extend(data.encode())
            client_socket.send(frame)
        except Exception as e:
            print(f"Error al enviar datos: {e}")

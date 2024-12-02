let socket;

function connectWebSocket() {
    const ipInput = document.getElementById("ip").value;
    const portInput = document.getElementById("port").value;
    const statusDiv = document.getElementById("status");

    // Construir URL del WebSocket
    const wsUrl = `ws://${ipInput}:${portInput}/`;
    statusDiv.textContent = `Conectando a ${wsUrl}...`;

    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        statusDiv.textContent = `Conectado a ${wsUrl}`;
        console.log("Conectado al servidor WebSocket");
    };

    socket.onmessage = (event) => {
        const packetsDiv = document.getElementById('packets');
        packetsDiv.innerHTML = '';
        try {
            const packets = JSON.parse(event.data);
            packets.forEach(packet => {
                const p = document.createElement('p');
                p.textContent = packet;
                packetsDiv.appendChild(p);
            });
        } catch (e) {
            console.error("Error al procesar los datos recibidos:", e);
        }
    };

    socket.onclose = () => {
        statusDiv.textContent = `Desconectado de ${wsUrl}. Reintentando...`;
        console.log("Desconectado del servidor WebSocket. Reintentando...");
        setTimeout(connectWebSocket, 2000); // Reintenta la conexión
    };

    socket.onerror = (error) => {
        statusDiv.textContent = `Error al conectar a ${wsUrl}. Verifica la IP y el puerto.`;
        console.error("Error en WebSocket:", error);
    };
}

function configureLoRa() {
    const frequency = document.getElementById("frequency").value;
    const bandwidth = document.getElementById("bandwidth").value;

    if (!socket || socket.readyState !== WebSocket.OPEN) {
        alert("Primero conecta al servidor WebSocket.");
        return;
    }

    const config = {
        action: "configure",
        frequency: parseInt(frequency, 10),
        bandwidth: parseInt(bandwidth, 10)
    };

    socket.send(JSON.stringify(config));
    console.log("Configuración enviada:", config);
}

function startScan() {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        alert("Primero conecta al servidor WebSocket.");
        return;
    }

    const command = { action: "start_scan" };
    socket.send(JSON.stringify(command));
    console.log("Comando enviado:", command);
}

function stopScan() {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        alert("Primero conecta al servidor WebSocket.");
        return;
    }

    const command = { action: "stop_scan" };
    socket.send(JSON.stringify(command));
    console.log("Comando enviado:", command);
}

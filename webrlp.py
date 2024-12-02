import webrepl
import comunes as c
import os 

def iniciar():
    # Intentar acceder a la configuración de WebREPL de manera diferente
    try:
        with open('/flash/webrepl.cfg', 'r'):
            c.Log("WebREPL ya está configurado.")
    except OSError:
        c.Log("Configurando WebREPL...")
        import webrepl_setup  # Configura WebREPL por código

    # Inicia WebREPL con la contraseña definida
    #webrepl.start(password='contrasena123')  # Contraseña de tu elección

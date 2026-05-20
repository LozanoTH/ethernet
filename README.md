# WPS Auditor PRO: Framework Modular de Auditoria Inalambrica

WPS Auditor PRO es una solucion avanzada y modular para la evaluacion de seguridad en redes inalambricas que utilizan el protocolo Wi-Fi Protected Setup (WPS). Diseñada con un enfoque primordial en la portabilidad para entornos Termux (Android) y sistemas GNU/Linux, esta herramienta integra un motor de inyeccion de paquetes con una interfaz de control remoto basada en web.

## 1. Arquitectura del Sistema

El proyecto ha sido refactorizado bajo una arquitectura modular para garantizar la escalabilidad, el mantenimiento simplificado y el aislamiento de fallos. La estructura se desglosa de la siguiente manera:

### 1.1 Modulos Principales (lib/)
*   **core.py (Motor de Auditoria)**: Orquesta la interaccion con el demonio `wpa_supplicant`. Gestiona el escaneo de redes mediante `iw`, el filtrado de objetivos y la maquina de estados para la negociacion de mensajes EAPOL/WPS (M1 a M8).
*   **web.py (Interfaz y API)**: Implementa un servidor HTTP asincrono que expone una API REST para el control del hardware. Gestiona el estado global de la aplicacion y sirve un Dashboard responsivo desarrollado en HTML5 y JavaScript.
*   **generator.py (Algoritmos de PIN)**: Biblioteca extensiva que contiene mas de 45 algoritmos de generacion de pines basados en el BSSID (MAC) y pines estaticos conocidos para fabricantes como TP-Link, Netgear, Belkin, D-Link y ASUS.
*   **utils.py (Servicios del Sistema)**: Centraliza la gestion de logs, la manipulacion de secuencias de escape ANSI para la terminal y las comprobaciones de entorno (Root, interfaces de red y sesiones SSH).

### 1.2 Punto de Entrada (wps.py)
Actua como el despachador de la aplicacion, procesando los argumentos de la linea de comandos y seleccionando el modo de operacion (Web o CLI).

## 2. Metodos de Auditoria Implementados

La herramienta soporta multiples vectores de ataque para la recuperacion de credenciales WPA/WPA2:

*   **Ataque Pixie Dust (Offline)**: Aprovecha debilidades en la generacion de numeros aleatorios (nonces) en ciertos chipsets para calcular el PIN WPS de forma casi instantanea sin necesidad de conexion continua con el AP.
*   **Ataque de PIN Estatico/Sugerido**: Utiliza la base de datos interna para probar pines conocidos vinculados al fabricante del dispositivo objetivo.
*   **Fuerza Bruta Inteligente**: Implementa un sistema de reanudacion de sesion para ataques de fuerza bruta en linea contra el protocolo WPS.

## 3. Instalacion y Despliegue

### 3.1 Entorno Termux (Android)
El despliegue en Termux esta simplificado mediante un script de gestion de ciclo de vida. Este script automatiza la verificacion de privilegios root y la consistencia de paquetes.

```bash
bash install.sh
```

### 3.2 Entorno GNU/Linux (Debian/Ubuntu/Kali)
Se requiere la instalacion manual de las dependencias del sistema:

```bash
sudo apt update
sudo apt install python3 wpasupplicant pixiewps iw
```

## 4. Manual de Operacion

### 4.1 Interfaz Web de Control Remoto
Al iniciar la aplicacion con el parametro `-W`, se habilita el panel de control accesible desde cualquier navegador en el dispositivo.

1.  **Panel de Redes**: Visualizacion jerarquica de puntos de acceso. Las redes se clasifican por vulnerabilidad conocida y estado de bloqueo WPS.
2.  **Consola de Eventos**: Pestaña dedicada al monitoreo en tiempo real de los logs del sistema. Permite observar el intercambio de llaves y la recepcion de la PSK.
3.  **Indicadores de Estado**: Un sistema de señalizacion visual (LED virtual) indica si el hardware esta en reposo, escaneando o ejecutando un ataque activo.

### 4.2 Referencia de Comandos CLI
| Parametro | Descripcion |
| :--- | :--- |
| `-i, --interface` | Especifica la interfaz de red inalambrica (ej. wlan0). |
| `-W, --web` | Inicia el servidor web de control remoto. |
| `--web-port` | Define el puerto TCP para la interfaz web (defecto: 8080). |
| `-K, --pixie-dust` | Habilita el modulo de ataque Pixie Dust. |
| `--demo` | Activa el modo de simulacion para pruebas sin hardware WiFi. |
| `-l, --loop` | Mantiene la ejecucion en bucle infinito para auditorias multiples. |

## 5. Especificaciones Tecnicas de Seguridad

*   **Deteccion de Sesion SSH**: El sistema incluye logica para detectar conexiones remotas y advertir al usuario antes de desconectar la interfaz de red, evitando la perdida de control del dispositivo.
*   **Gestion de Puertos**: El servidor web implementa la reutilizacion de sockets (SO_REUSEPORT) para garantizar reinicios rapidos en entornos de desarrollo.
*   **Aislamiento de Privilegios**: Aunque la herramienta requiere privilegios de superusuario para interactuar con el stack de red, el modulo de generacion de pines opera en un entorno restringido.

## 6. Descargo de Responsabilidad Legal

El uso de WPS Auditor PRO para acceder a redes sin autorizacion explicita es una actividad ilegal y penada por las leyes de ciberseguridad en la mayoria de las jurisdicciones. Esta herramienta ha sido desarrollada estrictamente para fines de investigacion, pruebas de penetracion autorizadas y educacion. El autor no asume responsabilidad alguna por daños o usos indebidos.

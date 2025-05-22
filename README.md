
# Comparación entre Máquina Virtual y Contenedor

## Introducción

### ¿Qué es una máquina virtual?

Una **máquina virtual (VM)** es un software que simula un ordenador completo dentro de otro ordenador. Se ejecuta sobre un **hipervisor** y tiene su propio sistema operativo, recursos virtualizados (CPU, memoria, disco, etc.), y puede funcionar como un equipo independiente.

### ¿Qué es un contenedor?

Un **contenedor** es una tecnología de virtualización más ligera que permite ejecutar aplicaciones de forma aislada pero compartiendo el mismo sistema operativo base del host. Usa una herramienta como **Docker**.

---

## Configuración de entorno de prueba

- **Máquina Host**:  
 GPU i5-1235U
 RAM 16GB
- **Máquina Virtual**:  
SO instalado: Ubuntu server 22.04 
Version VirtualBox: 7.0.16
Disco Virtual Asignado: 10GB 
Memoria RAM asignada: 2048 MB 
Nucleos CPU: 2 

- **Imagen base de Docker**:  
Imagen base: Ubuntu 22.04
Version de docker: 28.0.4
Recursos asignados: 2 nucleos CPU, 2GB RAM 

---

## Herramientas utilizadas

- **Sysbench**
- **Juego 2048 (Python)**

---

## Prueba en Sysbench

### Objetivo de la prueba

Comparar cuántas operaciones puede realizar la CPU en un mismo tiempo bajo ambos entornos:

- Docker (contenedor)
- VM (VirtualBox)

---

### Pasos de la prueba

#### 1. Instalación de Docker

- Descargar desde: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
- Ejecutar Docker
- Verificar versión:

```bash
docker --version
```

#### 2. Instalación de Sysbench

##### En Docker


- Ejecutar la prueba:

```bash
docker run --rm severalnines/sysbench sysbench cpu --threads=2 --time=30 run
```

##### En Máquina Virtual (Ubuntu)

- Conectarse a la VM (VirtualBox)
- Ejecutar:

```bash
sudo apt update
sudo apt install sysbench -y
sysbench cpu --cpu-max-prime=20000 run
```

---

## Resultados de la prueba en Sysbench (total de 5 pruebas)

| Entorno         | Hilos del procesador | Eventos por segundo  | Tiempo total (s) | Latencia promedio (ms)  | Número total de eventos |  
|-----------------|----------------------|----------------------|------------------|-------------------------|-------------------------| 
| Máquina Virtual |          2           |        6721          |        30        |          0.30           |          200999         | 
| Docker          |          2           |        6535          |        30        |          0.30           |           196175        |


## Prueba: Juego 2048

### Objetivo de la prueba

Comparar cuántas operaciones puede realizar la CPU en un mismo tiempo bajo ambos entornos:

- Docker (contenedor)
- VM (VirtualBox)

---

### Preparación

#### En Docker

- Imagen base con Node.js

**Dockerfile para ejecutar 2048-cli:**

```Dockerfile
FROM node:18-alpine
CMD ["npx", "2048-cli"]
```

- Ejecutar el juego:

```bash
docker build -t juego2048 .
docker run -it juego2048
```

#### En Máquina Virtual (Ubuntu)

- Instalar Node.js y npm:

```bash
sudo apt update
sudo apt install nodejs npm -y
```

- Ejecutar el juego:

```bash
npx 2048-cli
```

---

### Ejecución de pruebas de rendimiento

Mientras se ejecuta el juego, en otra terminal usar:

#### En Máquina Virtual

```bash
top
htop
vmstat 1
```

#### En Docker

```bash
docker stats <container_id>
```

---

## Resultados generales

| Métrica                         | VirtualBox (VM) | Docker |
|---------------------------------|-----------------|--------|
| Eventos por segundo             |                 |        |
| Tiempo total                    |                 |        |
| Número total de eventos ejecutados |             |        |
| Latencia (ms)                   |                 |        |

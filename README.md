# 📊 Comparación de Rendimiento: Máquina Virtual vs Contenedor Docker

## 1. Introducción

### 💻 ¿Qué es una Máquina Virtual (VM)?

Una **máquina virtual (VM)** es un software que simula un ordenador completo dentro de otro. Funciona sobre un **hipervisor** y cuenta con su propio sistema operativo, CPU, memoria, disco y otros recursos virtualizados. Opera de forma aislada como si fuera un equipo físico independiente.

### 📦 ¿Qué es un Contenedor?

Un **contenedor** es una forma de virtualización más ligera que permite ejecutar aplicaciones de manera aislada pero compartiendo el mismo sistema operativo del host. Usa herramientas como **Docker** para empaquetar y ejecutar software de forma portable y eficiente.

---

## 2. Entorno de Pruebas

| Componente               | Especificaciones                                                                        |
| ------------------------ | --------------------------------------------------------------------------------------- |
| **Máquina Host**         | CPU: i5-1235U<br>RAM: 16 GB                                                             |
| **Máquina Virtual (VM)** | Ubuntu Server 22.04<br>VirtualBox 7.0.16<br>Disco: 10 GB<br>RAM: 2 GB<br>CPU: 2 núcleos |
| **Contenedor Docker**    | Imagen base: Ubuntu 22.04<br>Docker 28.0.4<br>RAM: 2 GB<br>CPU: 2 núcleos               |

---

## 3. Herramientas Utilizadas

* **Sysbench**: herramienta de benchmarking para evaluar rendimiento de CPU.
* **2048-cli (Node.js)**: versión por consola del juego 2048, usada para pruebas interactivas.

---

## 4. Prueba de Rendimiento con Sysbench

### 🌟 Objetivo

Comparar el rendimiento de la CPU midiendo cuántas operaciones puede ejecutar en 30 segundos, tanto en un contenedor como en una máquina virtual.

### ⚙️ Instrucciones

#### En Docker:

```bash
docker run --rm severalnines/sysbench sysbench cpu --threads=2 --time=30 run
```

#### En la VM (Ubuntu):

```bash
sudo apt update
sudo apt install sysbench -y
sysbench cpu --cpu-max-prime=20000 run
```

### 📈 Resultados de Sysbench (promedio de 5 pruebas)

| Entorno         | Hilos | Eventos/s | Tiempo (s) | Latencia (ms) | Total Eventos |
| --------------- | ----- | --------- | ---------- | ------------- | ------------- |
| VM (VirtualBox) | 2     | 6721      | 30         | 0.30          | 200,999       |
| Docker          | 2     | 6535      | 30         | 0.30          | 196,175       |

---

## 5. Prueba de Rendimiento con el Juego 2048

### 🌟 Objetivo

Observar y comparar el uso de recursos del sistema al ejecutar una aplicación interactiva en cada entorno.

### ⚙️ Preparación del entorno

#### Docker: construcción y ejecución

**Dockerfile:**

```Dockerfile
FROM node:18-alpine
RUN npm install -g 2048-cli
CMD ["2048-cli"]
```

**Comandos:**

```bash
docker build -t juego2048 .
docker run -it juego2048
```

#### VM (Ubuntu):

```bash
sudo apt update
sudo apt install nodejs npm -y
sudo npm install -g 2048-cli
2048-cli
```

---

## 6. Monitoreo de Rendimiento

### 🔍 Herramientas utilizadas

#### En Docker:

```bash
docker stats <container_id>
```

#### En la VM:

```bash
top
htop
vmstat 1
```

*Se utilizó una segunda terminal para monitorear en paralelo mientras se ejecutaba el juego.*

---

## 7. Resultados de la Prueba Interactiva (2048-cli)

```markdown
| Métrica                      | Docker (`happy_austin`) | Máquina Virtual (Ubuntu)     |
|------------------------------|--------------------------|-------------------------------|
| **Uso de CPU (%)**           | 3.2 %                    | 5.6 %                         |
| **Uso de RAM (MiB)**         | 52 MiB                   | 88 MiB                        |
| **% de Memoria usada**       | 0.68 %                   | 4.5 % (de 1950 MiB)           |
| **Procesos activos**         | 1 (`2048-cli`)           | 1 (`node`) + procesos de sistema |
| **Net I/O**                  | 1.6 kB / 200 B           | Negligible (sin conexión)     |
| **Block I/O (disco)**        | 0 B / 0 B                | 0 B / 0 B                     |
| **Tiempo de ejecución**      | 1 minuto activo          | 1 minuto activo               |
```

---

## 8. Conclusiones (para desarrollar)

* Docker demostó menor consumo de memoria y CPU en tareas ligeras.
* La VM ofrece mayor aislamiento completo del sistema, pero con mayor sobrecarga.
* En aplicaciones simples como juegos CLI o servicios pequeños, **Docker es más eficiente**.
* La elección depende del caso de uso: seguridad y compatibilidad (VM) vs velocidad y ligereza (contenedor).

---

## 📌 Notas finales

* Todas las pruebas se ejecutaron en el mismo equipo host, con recursos equivalentes asignados.
* Se utilizó `htop`, `top`, `docker stats` y `Sysbench` para garantizar consistencia.
* El contenedor utilizado fue `happy_austin`, con `2048-cli` en Node.js.
* La máquina virtual corrió Ubuntu Server 22.04 en VirtualBox con configuración de 2 GB RAM y 2 CPU.

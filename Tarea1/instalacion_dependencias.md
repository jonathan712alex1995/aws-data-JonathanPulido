# Instalación de Dependencias en EC2 de AWS con Ubuntu

Guía para instalar Python v3.12, Docker, Docker Compose, Virtual Environment y Jupyter Notebook en una instancia EC2 de AWS con Ubuntu.

## Preparación Inicial

Antes de realizar las instalaciones, ejecutar los siguientes comandos:

```bash
sudo apt update
sudo apt upgrade
```

---

## 1. Instalación de Python

### 1.1 Verificación de Python

Python viene instalado por defecto en Ubuntu. Verificar la instalación con:

```bash
python3 --version
```

---

## 2. Instalación de Docker y Docker Compose

### 2.1 Instalar dependencias necesarias

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

### 2.2 Crear directorio keyrings

```bash
sudo mkdir -p /etc/apt/keyrings
```

### 2.3 Descargar y guardar la llave GPG de Docker

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

### 2.4 Modificar permisos al keyring

```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

### 2.5 Agregar el repositorio de Docker

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu jammy stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 2.6 Actualizar e instalar Docker

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 2.7 Verificar instalación de Docker

```bash
docker --version
```

Deberías obtener algo similar a:
```
Docker version 28.5.0, build 887030f
```

### 2.8 Verificar instalación de Docker Compose

```bash
docker compose version
```

---

## 3. Instalación de Virtual Environment

**Requisitos previos:** Python3 viene instalado por defecto pero debemos instalar pip:

```bash
sudo apt install python3-pip
```

Verificar la instalación:

```bash
pip3 --version
```

### 3.1 Instalación de virtualenv (usando pip)

```bash
pip3 install --user virtualenv
```

### 3.2 Agregar al PATH

```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

### 3.3 Instalar python3-virtualenv

```bash
sudo apt install python3-virtualenv
```

Verificar la instalación:

```bash
virtualenv --version
```

Deberías ver algo similar a:
```
virtualenv 20.25.0+ds
```

### 3.4 Verificar funcionamiento de virtualenv

#### 3.4.1 Crear un entorno virtual

```bash
virtualenv venv
```

#### 3.4.2 Activar el entorno virtual

```bash
source venv/bin/activate
```

Al ejecutarlo, tu prompt se verá así:
```
(venv) ubuntu@ip-172-31-
```

#### 3.4.3 Salir del entorno virtual

```bash
deactivate
```

---

## 4. Instalación de Jupyter (en un entorno virtual)

### 4.1 Crear un nuevo entorno virtual

```bash
virtualenv jupyter_env
source jupyter_env/bin/activate
```

### 4.2 Instalar Jupyter

Dentro del entorno virtual, ejecutar:

```bash
pip install jupyter
```

### 4.3 Verificar instalación de Jupyter

```bash
jupyter --version
```

> **Nota:** También puedes instalar Jupyter en el entorno creado anteriormente accediendo con `source ~/venv/bin/activate` y ejecutando el comando de instalación de Jupyter.

---

## Documentación de Referencia

- [Docker - Instalación en Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Virtualenv - PyPI](https://pypi.org/project/virtualenv/)
- [Jupyter - Instalación](https://jupyter.org/install)

---

# Enviar dataset desde nuestro equipo al EC2 de AWS

Debemos mover nuestro dataset a la misma carpeta en la que tenemos nuestro archivo.pem y ejecutar el siguiente comando

```bash
scp -i mi-clave.pem datos.csv ubuntu@3.123.45.67:/home/ubuntu/
```
En mi caso el comando correcto es el siguiente:

```bash
scp -i aws-data-jonathanPulido.pem netflix_titles.csv ubuntu@ec2-52-53-188-42.us-west-1.compute.amazonaws.com:/home/ubuntu/
```
Ahora solo debemos conectar a nuestro EC2 AWS y ejecutar el comando ls y veremoe el archivo que acabamos de mandar
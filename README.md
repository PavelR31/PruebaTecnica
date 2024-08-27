# Prueba Técnica

## Descripción

Prueba Técnica es una aplicación desarrollada en Laravel. Este documento proporciona instrucciones para configurar y ejecutar el proyecto en un entorno local.

## Requisitos

- [PHP](https://www.php.net/manual/en/install.php)
- [Composer](https://getcomposer.org/)
- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)

## Configuración del Entorno

### 1. Configuración del Entorno Python

1. **Accede al directorio de scripts**:
    ```bash
    cd /scripts
    ```

2. **Crea un entorno virtual**:
    ```bash
    python -m venv venv
    ```

3. **Activa el entorno virtual**:

    - **Windows PowerShell**:
      ```powershell
      .\venv\Scripts\Activate.ps1
      ```

    - **Windows Command Prompt**:
      ```cmd
      .\venv\Scripts\activate
      ```

4. **Instala las dependencias de Python**:
    ```bash
    pip install -r .\requisitos.txt
    ```

### 2. Configuración de la Aplicación

1. **Renombra el archivo `.env.example` a `.env`**.

2. **Instala las dependencias de PHP**:
    ```bash
    composer install
    ```
3. **Genera la clave de la aplicación**:
    ```bash
    php artisan key:generate
    ```
4. **Instala las dependencias de Node.js**:
    ```bash
    npm install
    ```

### 3. Ejecutar la Aplicación

1. **Compila los activos**:
    ```bash
    npm run dev
    ```

2. **Inicia el servidor de Laravel**:
    ```bash
    php artisan serve
    ```

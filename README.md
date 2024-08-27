# Prueba Técnica

## Descripción

Prueba Técnica es una aplicación desarrollada en Laravel. 
Este documento proporciona instrucciones para configurar y ejecutar el proyecto en un entorno local.

## Requisitos

- [PHP](https://www.php.net/manual/en/install.php) 
- [Composer](https://getcomposer.org/) 
- [Node.js](https://nodejs.org/) 
- [Python](https://www.python.org/) 

## Configuración del Entorno

### 1. Editar el archivo `.env.example`

Renombra el archivo `.env.example` a `.env`.

### 2. Configurar el entorno python
-Acceder al escritorio scripts[cd /scripts], estando ahí ejecutar los siguientes comandos en el siguiente orden:
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r .\requisitos.txt

### 3.  Configuración de la Aplicación
-Debemos instalar las dependencias de nodejs y las de PHP y generar la key.
    php artisan key:generate
    composer install
    npm install

### 4. Ejecutar la Aplicación
-Ejecutamos
    npm run dev
    php artisan serve


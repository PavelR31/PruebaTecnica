<?php
namespace App\Services;

class procesarPython
{
    public function ejecutarScript($url)
    {
        // Ruta al archivo de activación del entorno virtual en Windows
        $rutaVenv = base_path('scripts/venv/Scripts/activate.bat');

        // Crear el comando para activar el entorno virtual y ejecutar el script
        $comando = "\"$rutaVenv\" && python " . base_path('scripts/script.py') . " " . escapeshellarg($url);

        // Ejecutar el comando utilizando shell_exec
        $salida = shell_exec($comando);

        // Limpiar caracteres inválidos
        $salida = mb_convert_encoding($salida, 'UTF-8', 'auto');

        // Decodificar el JSON resultante
        $resultadoJson = json_decode($salida, true);

        return $resultadoJson;
    }
}

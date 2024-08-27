<?php
namespace App\Services;

use Illuminate\Support\Facades\Log;

class procesarPython
{
    public function ejecutarScript($url)
    {
        try {
            // Ruta al archivo de activación del entorno virtual en Windows
            $rutaVenv = base_path('scripts/venv/Scripts/activate.bat');
            $rutaScript = base_path('scripts/script.py');
            
            // Comando para activar el entorno virtual y ejecutar el script
            // Note the double quotes around paths with spaces
            $comando = "cmd.exe /c \"\"$rutaVenv\" && python \"$rutaScript\" " . escapeshellarg($url) . "\"";
            
            // Ejecutar el comando utilizando shell_exec
            $salida = shell_exec($comando);
            
            // Verificar si la salida es válida
            if ($salida === null) {
                Log::error('Error al ejecutar el comando: ' . $comando);
                return null;
            }
            
            // Limpiar caracteres inválidos y decodificar el JSON resultante
            $salida = mb_convert_encoding($salida, 'UTF-8', 'auto');
            $resultadoJson = json_decode($salida, true);
            
            if (json_last_error() !== JSON_ERROR_NONE) {
                Log::error('JSON Decode Error: ' . json_last_error_msg());
                return null;
            }
            
            return $resultadoJson;
        } catch (\Exception $e) {
            Log::error('Exception in ejecutarScript: ' . $e->getMessage());
            return null;
        }
    }
}

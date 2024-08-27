<?php

namespace App\Http\Controllers;

use App\Services\procesarPython;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class controladorExtraccion extends Controller
{
    protected $procesadorPython;

    public function __construct(procesarPython $procesadorPython)
    {
        $this->procesadorPython = $procesadorPython;
    }

    public function mostrarFormulario()
    {
        return view('welcome');
    }

    public function procesarSolicitud(Request $request)
    {
        $request->validate(['url' => 'required|url']);

        // Obtener la URL
        $url = $request->input('url');

        // Ejecutar el script a través del servicio
        $resultadoJson = $this->procesadorPython->ejecutarScript($url);

        // Validar si el resultado es null o un error
        if (is_null($resultadoJson)) {
            Log::error('Error al ejecutar el script o al decodificar JSON');
            return response()->json(['error' => 'Error al procesar la solicitud.'], 500);
        }

        // Retornar el resultado en caso de que todo salga bien
        return response()->json($resultadoJson);
    }
}

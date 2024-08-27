<?php

use App\Http\Controllers\controladorExtraccion;
use Illuminate\Support\Facades\Route;




Route::get('/', [controladorExtraccion::class, 'mostrarFormulario'])->name('mostrar.formulario');
Route::post('/procesar', [controladorExtraccion::class, 'procesarSolicitud'])->name('procesar.solicitud');

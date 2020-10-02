# SAT to X-SAT

Primera parte del proyecto del curso de complejidad y optimización en la Universidad del Valle sede Cali
Para su uso deben existir archivos SAT(.cnf) en la ruta InstanciasSAT y ejecutar el comando:

    bash reducir.sh -x x_sat

<dl>
    <dt>-x, -x_sat:</dt>
        <dd>Establece X-SAT de los archivos de salida.</dd>
        <dd>Se aceptan valores entre 3 y 10.</dd>
</dl>

<br />

Donde x_sat equivale a la reduccion deseada por ejemplo:

    bash reducir.sh -x 5

<br />

## Parámetros opcionales ##

Existen otros parámetros opcionales adicionales que permiten configurar variables en tiempos de ejecución:

    bash reducir.sh -x x_sat -t timeout -s solver -p processes

<dl>
    <dt>-t, --timeout:</dt>
    <dd>Establece tiempo máximo en segundos para la ejecución de cada archivo (por defecto: 240)</dd>
    <dd>Se aceptan valores positivos, en caso de ser cero o negativo se utilizara el valor por defecto.</dd>
    <dt>--s, --solver:</dt>
    <dd>Establece el solucionador de SAT utilizado (por defecto: glucose4).</dd>
    <dd>En caso de ingresar un valor no disponible se utilizara el valor por defecto.</dd>
    <dd>Disponibles: lingeling, glucose3, glucose4, cadical, maplechrono, maplecm, maplesat, minicard, minisat22 y minisatgh.</dd>
    <dt>-p, --processes:</dt>
    <dd>Establece la cantidad de hilos utilizados (por defecto: maxima cantidad de hilos disponibles).</dd>
    <dd>Se aceptan valores entre 1 y la máxima cantidad de hilos disponibles.</dd>    
    <dd>En caso de ingresar un valor invalido se utilizara el valor por defecto.</dd>
</dl>

<br />

A continuación se presentara un ejemplo del uso de parámetros adicionales:

    bash reducir.sh -x 5 -t 240

<br />

## Informacion adicional ##

El resultado de la ejecución se almacena en la carpeta X-SAT, que se crea de manera automática al momento de la ejecución.
Si se enviá un valor negativo, vació o igual a 0 se tomara el valor por defecto.

Este proyecto funciona correctamente en Linux o MacOS
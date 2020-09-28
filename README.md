# SAT-to-X-SAT
Primera parte del proyecto del curso de complejidad y optimización en la Universidad del Valle sede Cali
Para su uso deben existir archivos SAT(.cnf) en la ruta InstanciasSAT y ejecutar el comando:

bash reducir.sh -x x-sat

Donde x-sat equivale a la reduccion deseada por ejemplo:

bash reducir.sh -x 5

El resultado del proceso se muestra en la carpeta X-SAT, adicionalmente a esto existe un parametro opcional adicional -t donde se puede definir el tiempo maximo de ejecucion para cada archivo del directorio InstanciasSAT en segundos (el valor por defecto es 4 minutos), por ejemplo:

bash reducir.sh -x 5 -t 240

Si se envia un valor negativo, vacio o igual a 0 se tomara el valor por defecto.

Este proyecto funciona correctamente en Linux o MacOS

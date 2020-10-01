#!/bin/bash

while getopts :x:t:s: flag
do
    case "${flag}" in
        x) 
            x_value=$OPTARG
            ;;
        t)
            t_value=$OPTARG
            ;;
        s)
            s_value=$OPTARG
            ;;
        \?)
            echo "Opción inválida: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Opción -$OPTARG requiere un argumento." >&2
            exit 1
            ;;
    esac
done

if [[ $x_value == "" ]] ; then
    echo "Opcion -x es requerida." >&2; exit 1
fi

re='^[0-9]+$'
if ! [[ $x_value =~ $re ]] ; then
    echo "No es un número valido, solo se aceptan numeros entre 3 y 10." >&2; exit 1
fi

if [[ $t_value == "" ]] ; then
    t_value="240"
fi

pip3 install python-sat wrapt_timeout_decorator
python3 main.py $x_value $t_value $s_value

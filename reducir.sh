while getopts :x: flag
do
    case "${flag}" in
        x) 
            re='^[0-9]+$'
            if ! [[ $OPTARG =~ $re ]] ; then
                echo "No es un número valido, solo se aceptan numeros entre 3 y 10." >&2; exit 1
            fi

            pip3 install python-sat
            python3 ./main.py $OPTARG
            exit 1
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


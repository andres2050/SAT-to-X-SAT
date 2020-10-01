#!/bin/bash

# Andres Felipe Herrera Moreno - 1710150
# Donald Marcelo Catañeda - 1810034
# Jose Alexander Muñoz - 1810206

PYTHON3_REF=$(command -v python3)
PYTHON_REF=$(command -v python)
PYTHON_COMMAND=$PYTHON3_REF

if [[ -x $PYTHON3_REF ]]; then
  PYTHON_COMMAND=$PYTHON3_REF
elif [[ -x $PYTHON_REF ]]; then
  PYTHON_COMMAND=$PYTHON_REF
else
  echo "No se encontro una version de python 3.6+ de 64 Bits instalado."
  exit 1
fi

verify=$($PYTHON_COMMAND verify.py)
if [ -n "$verify" ]; then
  echo $verify
  exit 1
fi

$PYTHON_COMMAND main.py $@

#!/bin/bash
cd /Users/maximilianotombolini/Desktop/Royal\ Moto\ Service/Royal-Software/
python3 app.py &
sleep 20  # Espera 5 segundos para asegurar que el servidor haya iniciado
open http://127.0.0.1:5000/  # macOS

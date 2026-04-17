# Pre-commit Script para verificar antes de subir
#!/bin/bash

echo "🔍 Verificando código antes de commit..."

# Crear directorio si no existe
if [ ! -d "api" ]; then
    echo "❌ Error: Falta la carpeta 'api'"
    exit 1
fi

if [ ! -d "public" ]; then
    echo "❌ Error: Falta la carpeta 'public'"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Falta 'requirements.txt'"
    exit 1
fi

if [ ! -f "vercel.json" ]; then
    echo "❌ Error: Falta 'vercel.json'"
    exit 1
fi

echo "✅ Estructura verificada"
echo "✅ Listo para hacer push a GitHub"

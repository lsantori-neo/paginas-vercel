# 🔄 Conciliador General de Planillas - Vercel Edition

Aplicación web para conciliar y comparar dos archivos (CSV o Excel). Construida con **FastAPI** (backend) y **HTML/JavaScript** (frontend), optimizada para **Vercel**.

## 📋 Características

- ✅ Carga de dos archivos (CSV o Excel)
- 🔍 Detección de coincidencias
- ❌ Identificación de registros solo en tabla A
- ⚠️ Identificación de registros solo en tabla B
- 📊 Detección de diferencias en valores
- 📥 Descarga de reporte en Excel
- 🎨 Interfaz moderna y responsive

## 🚀 Deployment en Vercel

### Prerequisitos
- Cuenta en [Vercel](https://vercel.com)
- GitHub conectado a Vercel
- Git instalado localmente

### Pasos para subir a Vercel

#### 1. Preparar el repositorio Git
```bash
cd conciliador_vercel_production

# Inicializar git si no lo está
git init

# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit: Conciliador app for Vercel"
```

#### 2. Crear repositorio en GitHub
- Ve a [github.com/new](https://github.com/new)
- Crea un repositorio nombrado `conciliador-app` (o como prefieras)
- **NO** inicialices con README (ya tienes archivos locales)
- Copia la URL HTTPS del repositorio

#### 3. Conectar repositorio local a GitHub
```bash
# Reemplaza con tu URL de GitHub
git remote add origin https://github.com/TU_USUARIO/conciliador-app.git

# Enviar código a GitHub
git branch -M main
git push -u origin main
```

#### 4. Conectar y Deployar en Vercel
Opción A - Desde CLI:
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deployar
vercel
```

Opción B - Desde Dashboard:
- Ve a [vercel.com/dashboard](https://vercel.com/dashboard)
- Click "Add New..." → "Project"
- Selecciona tu repositorio de GitHub
- Vercel detectará automáticamente que es Python con FastAPI
- Click "Deploy"

#### 5. Configuración en Vercel (si es necesaria)
En las opciones de deployment:
- **Framework Preset**: Other
- **Build Command**: `pip install -r requirements.txt` (automático)
- **Install Command**: (dejar en blanco, se usa pip por defecto)
- **Output Directory**: (dejar en blanco)

### ✅ ¡Listo!
Tu aplicación estará en vivo en: `https://tu-app-name.vercel.app`

## 🏠 Uso Local

### Sin Docker
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn api.main:app --reload

# Abrir navegador en http://localhost:8000
```

### Con Docker (opcional)
```bash
docker build -t conciliador .
docker run -p 8000:8000 conciliador
```

## 📁 Estructura del Proyecto

```
conciliador_vercel_production/
├── api/
│   └── main.py              # Backend FastAPI
├── public/
│   └── index.html           # Frontend HTML/JS
├── vercel.json              # Configuración Vercel
├── requirements.txt         # Dependencias Python
├── package.json             # Metadatos del proyecto
├── .gitignore               # Archivos a ignorar en Git
└── README.md                # Este archivo
```

## 🔧 Troubleshooting

### Error: "Module not found"
- Verifica que `requirements.txt` está actualizado
- En Vercel, ve a Settings → Environment Variables y asegúrate de que no hay conflictos

### La aplicación no carga archivos
- Verifica que Vercel está ejecutando Python 3.11+
- En `vercel.json`, el runtime debe ser `python3.11`

### CORS errors
- El backend FastAPI ya tiene CORS configurado
- Si aún así recibes errores, verifica la configuración en `api/main.py`

### Excel no se descarga correctamente
- Instala `openpyxl`: incluido en `requirements.txt`
- Si sigue sin funcionar, en Vercel aumenta el `timeout` en `vercel.json`

## 📝 Variables de Entorno (si aplica)

Actualmente no se requieren, pero puedes agregar en Vercel Dashboard:
- Settings → Environment Variables
- Agregar según necesidad (ej: logging, etc.)

## 🔒 Seguridad

Consideraciones para producción:
1. ✅ CORS está configurado (pero acepta `*`, considera restringir)
2. ✅ File size limits no están implementados (considera agregar)
3. ✅ No hay autenticación (considera agregar si es necesario)

Para producción segura:
```python
# En api/main.py, modifica CORS:
allow_origins=["https://tu-dominio.com"]
```

## 📦 Actualizar el código

Después de hacer cambios locales:
```bash
git add .
git commit -m "Tu mensaje de cambio"
git push origin main
```

Vercel se redesplegará automáticamente cada vez que hagas push a main.

## 📞 Soporte

Si encuentras errores:
1. Verifica los logs en Vercel Dashboard → Deployments → Logs
2. Revisa el navegador (F12) para ver errores de frontend
3. Comprueba que todas las dependencias en `requirements.txt` estén correctas

## 📄 Licencia

MIT - Siéntete libre de usar y modificar

---

**¿Necesitas ayuda?** Revisa la [documentación de Vercel](https://vercel.com/docs) o [FastAPI](https://fastapi.tiangolo.com/)

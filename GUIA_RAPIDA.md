# ⚡ GUÍA RÁPIDA - SUBIR A VERCEL EN 5 MINUTOS

## Paso 1: Prepare su Git (1 minuto)
```bash
cd conciliador_vercel_production
git init
git add .
git commit -m "Proyecto Conciliador Vercel"
```

## Paso 2: Crear repositorio en GitHub (1 minuto)
1. Ve a https://github.com/new
2. Nombra: `conciliador-app`
3. Click "Create repository"
4. Copia la URL HTTPS

## Paso 3: Conectar GitHub (1 minuto)
```bash
git remote add origin https://github.com/TU_USUARIO/conciliador-app.git
git branch -M main
git push -u origin main
```

## Paso 4: Deployar en Vercel (2 minutos)
Opción A - Lo más fácil:
- Ve a https://vercel.com/dashboard
- Click "Add New..." → "Project"
- Selecciona tu repositorio
- Click "Deploy"

Opción B - Desde Terminal:
```bash
npm i -g vercel
vercel
```

## ✅ ¡Listo!
Tu app estará en: `https://tu-proyecto.vercel.app` 🎉

---

## 🆘 Problemas comunes

**"Module not found"**
→ Verifica que `requirements.txt` está en la raíz

**"No puedo subir archivos"**
→ Revisa la consola del navegador (F12)

**"La descarga Excel no funciona"**
→ Espera 30 segundos más, Vercel se está iniciando

---

Necesitas más ayuda? Lee el **README.md** completo.

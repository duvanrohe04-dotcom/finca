# 🌿 Finca Admin

Panel de administración para gestión de finca ganadera.

## Requisitos

- Python 3.8+
- pip

## Instalación

1. **Crear entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

4. **Abrir en el navegador:**
   ```
   http://localhost:5000
   ```

## Credenciales por defecto

| Campo    | Valor    |
|----------|----------|
| Usuario  | admin    |
| Contraseña | admin123 |

> ⚠️ Cambia la contraseña desde **Configuración** después del primer inicio de sesión.

## Módulos

| Módulo        | Descripción                                              |
|---------------|----------------------------------------------------------|
| Dashboard     | Resumen general con estadísticas del sistema             |
| Ganado        | Registro de ganado adulto y terneros con padres/madres  |
| Obreros       | Control de trabajadores, días y cálculo de nómina        |
| Inventario    | Bultos (concentrado, sal, etc.) y medicamentos con totales |
| Leche         | Registro diario de litros (mañana/tarde) e ingresos      |
| Configuración | Cambio de datos del administrador y contraseña           |

## Estructura del proyecto

```
finca/
├── app.py              # Configuración principal de Flask
├── models.py           # Modelos de base de datos (SQLAlchemy)
├── requirements.txt    # Dependencias
├── routes/
│   ├── auth.py         # Login/logout
│   ├── dashboard.py    # Panel principal
│   ├── ganado.py       # CRUD ganado y terneros
│   ├── obreros.py      # CRUD obreros
│   ├── inventario.py   # CRUD inventario (bultos y drogas)
│   ├── leche.py        # CRUD registros de leche
│   └── configuracion.py # Ajustes del admin
├── templates/          # Plantillas HTML (Jinja2)
└── static/
    ├── css/style.css   # Estilos
    └── js/main.js      # JavaScript
```

## Base de datos

Usa SQLite. El archivo `instance/finca.db` se crea automáticamente al primer inicio.
Para reiniciar los datos, borra el archivo `instance/finca.db` y reinicia la app.

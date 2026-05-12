# ============================================================
#  conf/gunicorn.conf.py
#  Configuración de Gunicorn para producción
#  (Opcional: usa esto en lugar de app.run() en producción)
# ============================================================

import os

bind       = f"0.0.0.0:{os.getenv('PORT', '81')}"
workers    = 2          # Ajusta según CPU disponibles (2 × núcleos + 1)
threads    = 2
timeout    = 120
loglevel   = "info"
accesslog  = "-"        # stdout
errorlog   = "-"        # stderr

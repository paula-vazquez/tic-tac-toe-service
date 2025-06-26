from dotenv import load_dotenv
import os

# 1) Carga automáticamente el primer .env que encuentre en CWD o sus padres
load_dotenv()

class Settings:
    # Si la variable no existe, devolvemos cadena vacía
    DB_URL: str = os.getenv("DB_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    def validate(self):
        missing = []
        if not self.DB_URL:
            missing.append("DB_URL")
        if not self.SECRET_KEY:
            missing.append("SECRET_KEY")
        if missing:
            raise RuntimeError(f"Faltan variables de entorno: {', '.join(missing)}")

# Instancia y validación al importar
settings = Settings()
settings.validate()

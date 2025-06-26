from fastapi import FastAPI
from config.settings import settings

app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "database": settings.DB_URL,
        "secret_key_length": len(settings.SECRET_KEY)
    }

if __name__ == "__main__":
    from adapters.print_core import run
    run()
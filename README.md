# Tic-Tac-Toe Service

Servicio web de Tic-Tac-Toe implementado con FastAPI, SQLAlchemy y PostgreSQL.

## Autora

- Nombre: **Paula Vázquez Tella**  
- Fecha: **26/06/2025**

## Supuestos

- Las coordenadas de casilla (`x`, `y`) se envían **1-indexadas** (valores de 1 a 3).  
- No hay autenticación de usuarios (parte 2 pendiente de diseño, no implementada).  
- Variables sensibles gestionadas vía archivo `.env` en la raíz.  
- El servicio es **stateless**; cada petición proporciona todo lo necesario.  
- Logging básico a stderr con niveles INFO/DEBUG/ERROR.

## Requisitos

- Python **3.12+**  
- PostgreSQL (local o en contenedor Docker)  
- Git

## Instalación y configuración

1. **Clona el repositorio**  

   git clone <https://github.com/paula-vazquez/tic-tac-toe-service.git>
   
   cd tic-tac-toe-service

3. **Crea y activa un entorno virtual**  

   python -m venv venv
   **Linux / macOS**
   source venv/bin/activate
   **Windows PowerShell**
   .\venv\Scripts\Activate.ps1

4. **Instala dependencias**  

   pip install --upgrade pip
   pip install -r requirements.txt

5. **Configura variables de entorno**  
   En la raíz crea un fichero `.env` con al menos:

   DB_URL=postgresql://postgres:postgres@localhost:5432/tictactoe
   
   SECRET_KEY=UnaCadenaMuySecretaDeAlMenos32Caracteres

## Migraciones

1. Asegúrate de que PostgreSQL está en marcha y existe la base de datos `tictactoe`.  
2. Ejecuta las migraciones con Alembic:

   alembic upgrade head

## Arranque del servidor

uvicorn main:app --reload --app-dir src --host 127.0.0.1 --port 8000

- `--reload` recarga al detectar cambios.  
- `--app-dir src` indica que el código está en la carpeta `src/`.

## Uso de la API

### 1. Crear una nueva partida

**POST** `/create`

curl -X POST http://127.0.0.1:8000/create

**Respuesta de ejemplo**  

{ "matchId": "e2f1c3a4-5678-90ab-cdef-1234567890ab" }


### 2. Jugar un movimiento

**POST** `/move`

curl -X POST http://127.0.0.1:8000/move \
  -H "Content-Type: application/json" \
  -d '{
        "matchId": "e2f1c3a4-5678-90ab-cdef-1234567890ab",
        "playerId": "X",
        "square": { "x": 1, "y": 1 }
      }'

**Respuesta de ejemplo**  
{
  "board": [
    ["X", "", ""],
    ["", "", ""],
    ["", "", ""]
  ],
  "status": "IN_PROGRESS",
  "next_player": "O"
}

### 3. Consultar el estado de la partida

**GET** `/status?matchId=<matchId>`

curl "http://127.0.0.1:8000/status?matchId=e2f1c3a4-5678-90ab-cdef-1234567890ab"


**Respuesta de ejemplo**  
{
  "board": [
    ["X", "", ""],
    ["", "", ""],
    ["", "", ""]
  ],
  "status": "IN_PROGRESS",
  "next_player": "O"
}

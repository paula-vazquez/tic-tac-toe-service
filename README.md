# Tic-Tac-Toe Service

Servicio web de Tic-Tac-Toe implementado con FastAPI, SQLAlchemy y PostgreSQL.

## Autora
- Nombre: **Paula Vázquez Tella**  
- Fecha: **26/06/2025**

## Supuestos
- Las coordenadas de casilla (`x`, `y`) se envían **1-indexadas** (valores de 1 a 3).  
- El servicio es **stateless**; cada petición proporciona todo lo necesario.  
- Logging básico a stderr con niveles INFO/DEBUG/ERROR.
- Implementación de un frontend funcional.
- No hay autenticación de usuarios (parte 2 pendiente de diseño, no implementada).  
- Variables sensibles gestionadas vía archivo `.env` en la raíz.  

## Requisitos
- Python **3.12+**  
- PostgreSQL (local o en contenedor Docker)  
- Git

## Instalación y configuración

### Usando Docker (Recomendado)
1. **Clona el repositorio**  

   git clone https://github.com/paula-vazquez/tic-tac-toe-service.git

   cd tic-tac-toe-service

2. **Levanta los contenedores Docker**  

   docker-compose up --build

   Este comando descargará las imágenes necesarias, construirá el contenedor de la aplicación web y levantará la base de datos PostgreSQL, asegurándose de que todo funcione correctamente.

3. **Accede a la aplicación**  
   Una vez que Docker haya levantado los contenedores, podrás acceder a la API en [http://localhost:8000](http://localhost:8000).

### Sin Docker (Alternativa)
1. **Crea y activa un entorno virtual**  

   python -m venv venv

   # Linux -> source venv/bin/actívate

   # Windows -> .env\Scripts\Activate.ps1

2. **Instala dependencias**  

   pip install --upgrade pip

   pip install -r requirements.txt

3. **Configura variables de entorno**  
   En la raíz crea un fichero `.env` con al menos:

   DB_URL=postgresql://postgres:postgres@localhost:5432/tictactoe

   SECRET_KEY=UnaCadenaMuySecretaDeAlMenos32Caracteres

4. **Configura y ejecuta las migraciones de la base de datos**  

   alembic upgrade head

### Arranque del servidor
Ejecuta el servidor con FastAPI:

uvicorn main:app --reload --app-dir src --host 127.0.0.1 --port 8000

## Migraciones
1. Asegúrate de que PostgreSQL está en marcha y existe la base de datos `tictactoe`.  
2. Ejecuta las migraciones con Alembic:

   alembic upgrade head

## Uso de la API

### 1. Crear una nueva partida
**POST** `/create`

curl -X POST http://127.0.0.1:8000/create

**Respuesta de ejemplo**  

{ "matchId": "e2f1c3a4-5678-90ab-cdef-1234567890ab" }

### 2. Jugar un movimiento
**POST** `/move`

curl -X POST http://127.0.0.1:8000/move   -H "Content-Type: application/json"   -d '{
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

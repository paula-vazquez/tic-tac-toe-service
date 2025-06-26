# Documentación Técnica — Decisiones de Diseño

## Índice

1. [Clean Architecture](#clean-architecture)  
2. [Twelve-Factor App](#twelve-factor-app)  
3. [Decisión del Frontend “mini”](#decisión-del-frontend-mini)  


## Clean Architecture

**Objetivo**: Separar responsabilidades para lograr un código fácil de mantener y escalar.

- **Capa Core (Dominio)**  
  - **Entidades** (`core/models.py`): representación pura de `Match`, `Player`, `Square`, `MatchStatus`.  
  - **Casos de uso** (`core/usecases.py`): `CreateMatch`, `MakeMove`, `GetStatus`.  
  - **Beneficio**: Lógica de negocio totalmente desacoplada de frameworks, base de datos o infraestructuras externas.

- **Capa Adapters (Infraestructura)**  
  - **Repositorios** (`adapters/sql_match_repository.py`): implementan interfaz `MatchRepository` usando SQLAlchemy.  
  - **Modelos ORM** (`adapters/models.py`) y **DB** (`adapters/db.py`): persistencia aislada.  
  - **Beneficio**: Si mañana cambiamos de PostgreSQL a otra base de datos, bastaría con sustituir este adapter.

- **Capa Framework (FastAPI)**  
  - **`src/main.py`** expone los endpoints HTTP y convierte peticiones a casos de uso.  
  - **Schemas Pydantic** (`schemas.py`) validan y serializan la entrada/salida.  
  - **Beneficio**: El framework sólo convive en esta capa; el núcleo de la app no depende de FastAPI.


## Twelve-Factor App

Aplicando buenas prácticas de [12-Factor](https://12factor.net):

1. **Codebase**:  
   - Un único repositorio Git, con ramas `main` (estable) y `develop` (integración).  
2. **Configuración**:  
   - Variables (`.env`) gestionadas con **python-dotenv**, nunca en el código.  
3. **Dependencias**:  
   - `requirements.txt` generado con `pip freeze`.  
4. **Backing Services**:  
   - PostgreSQL tratado como un servicio adjunto, configurable vía `DB_URL`.  
5. **Build, Release, Run**:  
   - Separación clara:  
     - **Build**: instalación pip y generación de migraciones.  
     - **Release**: etiqueta Git `vX.Y.Z`.  
     - **Run**: arranque con `uvicorn src.main:app`.  
6. **Dev/Prod Parity**:  
   - Dockerfile y `docker-compose.yml` opcionales facilitan réplica de entorno.  
7. **Logs**:  
   - Emitidos a STDERR usando el módulo `logging` (niveles INFO/DEBUG/ERROR).  
8. **Processes**:  
   - Servicio stateless; cada request abre una sesión y la cierra.
9. **Admin Processes**:  
   - Migraciones Alembic como proceso ad hoc (`alembic upgrade head`).


## Decisión del Frontend “mini”

> “Quería que este challenge no fuera sólo un ejercicio de backend, sino un demo completo de experiencia de juego.”

- **Por qué lo hice**  
  - **Visibilidad de resultado**: Un API sin UI es menos tangible. El pequeño SPA permite comprobar la lógica en tiempo real.  
  - **Completar el flujo**: Mostrar creación de partida, movimientos y estados finales sin usar `curl` o Postman.  
  - **Aprendizaje full-stack**: Demuestra capacidad para conectar FastAPI con JavaScript “vanilla” y estilo CSS moderno.

- **Qué me gusta del enfoque**  
  - **Simplicidad**: Solo HTML/CSS/JS, cero frameworks adicionales, fácil de entender y extender.  
  - **Flexibilidad**: Permite evolucionar a React/Vue cuando la app necesite real-time o más interacción.  
  - **UX básica**: Interfaz centrada, colores suaves y emojis que aportan un toque humano y “feedback” inmediato al usuario.


> Con esta documentación separada capturo no solo **qué** hice, sino **por qué**: las decisiones están alineadas con buenas prácticas de arquitectura, configuración y usabilidad.

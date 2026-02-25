from app.database import async_session_maker
from app.clients.router import router as clients_router
# from app.operations.router import router as operations_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pathlib import Path
from sqlalchemy import text


app = FastAPI()
app.include_router(clients_router)
# app.include_router(operations_router)


origins = ['*',]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['Content-Type', 'Set-Cookie', 
                   'Access-Control-Allow-Headers', 
                   'Access-Control-Allow-Origin'],
)


# Временная ручка обновления бд
@app.post('/refresh_db/')
async def refresh_db():
    base_dir = Path(__file__).resolve().parent.parent
    sql_path = base_dir / 'data_for_postgre.sql'
    sql_script = sql_path.read_text(encoding='utf-8')
    async with async_session_maker() as session:
        async with session.begin():
            commands = sql_script.split(";")
            for command in commands:
                command = command.strip()
                if command:
                    await session.execute(text(command))

    return {'message': 'Database refreshed successfully'}
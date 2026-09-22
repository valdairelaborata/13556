from fastapi import FastAPI

import models
from database import initialize_database
from routers.clientes import router as clientes_router


app = FastAPI(title="API de clientes")
app.include_router(clientes_router)

initialize_database()

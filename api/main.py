from fastapi import FastAPI

from api.routes.equipment import router as equipment_router
from api.routes.sensors import router as sensors_router
from api.routes.alerts import router as alerts_router
from api.routes.prediction import router as prediction_router


app = FastAPI(
    title="Offshore Predictive Maintenance API",
    description="API educacional para monitoramento preditivo de bombas centrífugas.",
    version="1.0.0"
)

app.include_router(equipment_router)
app.include_router(sensors_router)
app.include_router(alerts_router)
app.include_router(prediction_router)


@app.get("/")
def inicio():
    return {
        "mensagem": "API Offshore Predictive Maintenance funcionando."
    }
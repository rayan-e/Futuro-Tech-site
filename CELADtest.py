from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI()

class SensorData(BaseModel):
    sensor_id: str
    value: float
    unit: str

    @field_validator("value")
    @classmethod
    def value_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("La valeur du capteur ne peut pas être négative")
        return v

class SensorResponse(BaseModel):
    status: str
    sensor_id: str
    message: str

@app.post("/sensors/data", response_model=SensorResponse)
async def receive_sensor_data(data: SensorData):
    if data.unit not in ["celsius", "bar", "rpm"]:
        raise HTTPException(status_code=400, detail="Unité non reconnue")

    return SensorResponse(
        status="ok",
        sensor_id=data.sensor_id,
        message=f"Valeur {data.value} {data.unit} enregistrée"
    )
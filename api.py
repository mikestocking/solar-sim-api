from fastapi import FastAPI
import glob
import re
import project

app = FastAPI()

#Example HTTP request: https://shiny-robot-xqpjxv9wg92pjrg-8000.app.github.dev/sites?site_id=9068&ghi=1050&dni=1000&dhi=100&temp_air=30&wind_speed=5&relative_humidity=50&local_time='20170401 1200'

@app.get("/sites")
async def root(local_time: str, site_id: int, ghi: int, dni: int, dhi: int, temp_air: float, wind_speed: float, relative_humidity: float):
    weather_params = {
        "local_time": local_time,
        "ghi": ghi,
        "dni": dni,
        "dhi": dhi,
        "temp_air": temp_air,
        "wind_speed": wind_speed,
        "relative_humidity": relative_humidity
        }
    return project.main(site_id, weather_params)


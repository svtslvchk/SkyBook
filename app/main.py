from fastapi import FastAPI

from app.routers.flight import router as router_flight
from app.routers.admin.flight import router as routers_flight_admin
from app.routers.airport import router as router_airport
from app.routers.admin.airport import router as router_airport_admin
from app.routers.airline import router as router_airline
from app.routers.admin.airline import router as router_airline_admin
from app.routers.aircraft import router as router_aircraft
from app.routers.admin.aircraft import router as router_aircraft_admin


app = FastAPI(
    title="SkyBook",
    description="Airline ticket booking and sales service",
    version="0.1.0"
)

app.include_router(router_flight)
app.include_router(routers_flight_admin)
app.include_router(router_airport)
app.include_router(router_airport_admin)
app.include_router(router_airline)
app.include_router(router_airline_admin)
app.include_router(router_aircraft)
app.include_router(router_aircraft_admin)

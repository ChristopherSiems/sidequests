from fastapi import APIRouter

from backend.database import create_POI
from backend.server.models.poi_create import POICreate

router = APIRouter()


@router.post("/pois", status_code=201)
def submit_poi(poi: POICreate):
  new_id = create_POI(
    title=poi.title,
    day=poi.day,
    open_time=poi.open_time,
    close_time=poi.close_time,
    location=poi.location,
    latitude=poi.latitude,
    longitude=poi.longitude,
    min_time=poi.min_time,
    link=poi.link,
    description=poi.description,
    categories=poi.categories,
    image=poi.image,
  )
  return {"id": new_id}

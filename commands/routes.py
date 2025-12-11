from fastapi import APIRouter
import requests

router = APIRouter()

@router.get("/precio/{item_id}")
def get_price(item_id: str):
    """ Devuelve precios en tiempo real desde Albion Data """
    url = f"https://www.albion-online-data.com/api/v2/stats/Prices/{item_id}"
    data = requests.get(url).json()
    return {
        "item": item_id,
        "data": data
    }

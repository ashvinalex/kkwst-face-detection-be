from fastapi import APIRouter
import requests
import yaml

credentials = yaml.load(open('credentials.yml'), Loader=yaml.Loader)
token = credentials['service']['service_token']
host = credentials['service']['service_host']

router = APIRouter(prefix='/service',
                   tags=["Service"],
                   responses={401: {"description": "Not Authorized"}})


@router.get("/start_service")
async def start_services():
    url = f"{host}/ai-model-service/start?api_token={token}"
    response = requests.post(url, json={})
    message = response.json()
    return message


@router.get("/service_status")
async def service_status():
    url = f"{host}/ai-model-service/status?api_token={token}"
    response = requests.post(url, json={})
    message = response.json()
    return message


@router.get("/stop_service")
async def stop_services():
    url = f"{host}/ai-model-service/stop?api_token={token}"
    response = requests.post(url, json={})
    message = response.json()
    return message

import httpx
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Union, Optional, Literal
from config import OPENWEATHER_API_KEY, OPENWEATHER_URL

app = FastAPI()
logging.basicConfig(level=logging.INFO)

class OpenWeatherMainValue(BaseModel):
    temp: Optional[float] = None

class OpenWeatherResponse(BaseModel):
    main: Optional[OpenWeatherMainValue] = None
    name: Optional[str] = None
    cod: Union[str, int]
    message: Optional[str] = None

class VapiArgumentsValue(BaseModel):
    city: str

class VapiFunctionValue(BaseModel):
    name: str
    arguments: VapiArgumentsValue

class VapiToolCall(BaseModel):
    id: str
    type: Literal["function"] = "function"
    function: VapiFunctionValue

class VapiMessageValue(BaseModel):
    toolCallList: list[VapiToolCall]

class VapiToolCallPayload(BaseModel):
    message: VapiMessageValue


@app.get("/")
def healthcheck():
    return JSONResponse(content={"status": "HealthCheck Success"})


@app.post("/api")
async def process_vapi_weather_tool(payload: VapiToolCallPayload) -> JSONResponse:
    """
    Takes in the Vapi tool call payload and calls the Open Weather API usig the
    city. Formats the response using the Vapi tool call ID and the Open Weather
    city and temp.

    Args:
        payload (VapiToolCallPayload): Vapi tool call payload.

    Returns:
        JSONResponse.
    """
    vapi_tool_call_id = payload.message.toolCallList[0].id
    vapi_city = payload.message.toolCallList[0].function.arguments.city
    
    weather_response = await call_openweather_api(vapi_city)
    if weather_response.cod != 200:
        return JSONResponse(content=format_vapi_response(vapi_tool_call_id, "Unable to get temperature"))
    
    weather_city = weather_response.name
    weather_temp = weather_response.main.temp
    
    if weather_city is None or weather_temp is None:
        return JSONResponse(content=format_vapi_response(vapi_tool_call_id, "Error with temperature or city."))
    
    return JSONResponse(content=format_vapi_response(vapi_tool_call_id, f"The weather in {weather_city} is a nice {weather_temp} degrees celsius."))


async def call_openweather_api(city: str) -> OpenWeatherResponse:
    """
    Calls the Open Weather API using the city from the Vapi tool call.

    Args:
        city (str).

    Returns:
        OpenWeatherResponse
    """
    try:
        async with httpx.AsyncClient() as client:
            url = OPENWEATHER_URL
            params = {
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            }
            openweather_response = await client.get(url=url, params=params)
            openweather_data = openweather_response.json()
            
            return OpenWeatherResponse(**openweather_data)
    except Exception as e:
        return OpenWeatherResponse(cod="error", message="Unable to retrieve temperature.")


def format_vapi_response(tool_call_id, message) -> dict:
    """
    Formats a response that Vapi expects, using the tool call ID from Vapi and the message
    dependent on the response type.

    Args:
        tool_call_id (_type_): Vapi tool call ID.
        message (_type_): Conditional message.

    Returns:
        dict: A Vapi-compatible format.
    """
    vapi_response = {
        "results": [
            {
                "toolCallId": tool_call_id,
                "result": message
            }
        ]
    }
    
    return vapi_response

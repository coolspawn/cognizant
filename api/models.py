# generated by fastapi-codegen:
#   filename:  ./docs/weather.yaml
#   timestamp: 2022-05-18T18:25:42+00:00

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, confloat, conint


class Cursor(BaseModel):
    __root__: Any = Field(
        ..., description='Cursor (timestamp)', example=7546416846.5555
    )


class Limit(BaseModel):
    __root__: Optional[conint(ge=1, le=300)] = Field(
        None, description='limit of rows in response', example=100
    )


class WeatherData(BaseModel):
    measure_date: Optional[datetime] = Field(
        None, description='Period', example='2021-07-21T17:32:28Z'
    )
    temperature: Optional[confloat(ge=-273.15, le=100.0)] = Field(
        None, description='Temperature Cel', example=35.5
    )
    pressure: Optional[confloat(ge=0.0)] = Field(
        None, description='Pressure HPA', example=1058.0
    )
    humidity: Optional[confloat(ge=0.0, le=100.0)] = Field(
        None, description='Humidity in percents', example=63.0
    )
    cloudiness: Optional[confloat(ge=0.0, le=8.0)] = Field(
        None, description='Cloudiness oktas', example=4
    )
    wind: Optional[confloat(ge=0.0)] = Field(None, description='Wind m/s', example=12.5)


class Error(BaseModel):
    error: Optional[str] = None
    error_description: Optional[str] = None


class Agg(Enum):
    median = 'median'
    highest = 'highest'
    lowest = 'lowest'


class Results(BaseModel):
    pass


class Capital(Enum):
    Vienna = 'Vienna'
    Brussels = 'Brussels'
    Sofia = 'Sofia'
    Zagreb = 'Zagreb'
    Nicosia = 'Nicosia'
    Prague = 'Prague'
    Copenhagen = 'Copenhagen'
    Tallinn = 'Tallinn'
    Helsinki = 'Helsinki'
    Paris = 'Paris'
    Berlin = 'Berlin'
    Athens = 'Athens'
    Budapest = 'Budapest'
    Dublin = 'Dublin'
    Rome = 'Rome'
    Riga = 'Riga'
    Vilnius = 'Vilnius'
    Luxembourg = 'Luxembourg'
    Valleta = 'Valleta'
    Amsterdam = 'Amsterdam'
    Warsaw = 'Warsaw'
    Lisbon = 'Lisbon'
    Bucharest = 'Bucharest'
    Bratislava = 'Bratislava'
    Ljubljana = 'Ljubljana'
    Madrid = 'Madrid'
    Stockholm = 'Stockholm'


class WeatherResult(BaseModel):
    city: Optional[str] = Field(None, description='European capital', example='Prague')
    weather_data: Optional[List[WeatherData]] = None


class ApiV1HistoricalDataCapitalGetResponse(BaseModel):
    limit: Optional[int] = Field(
        None, description='Rows limit per response', example=1000
    )
    cursor: Optional[float] = Field(
        None, description='Cursor', example=12345635877.11244
    )
    from_date: Optional[date] = Field(
        None, description='From period', example='2021-01-01'
    )
    till_date: Optional[date] = Field(
        None, description='Till period', example='2021-02-01'
    )
    aggregation: Optional[str] = Field(
        None, description='Aggregation type', example='median'
    )
    results: Optional[Union[List[WeatherResult], Results]] = None

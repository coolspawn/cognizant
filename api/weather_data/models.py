# generated by fastapi-codegen:
#   filename:  ./docs/weather.yaml
#   timestamp: 2022-05-18T18:25:42+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, confloat


class Cities(Enum):
    vienna = 'Vienna'
    brussels = 'Brussels'
    sofia = 'Sofia'
    zagreb = 'Zagreb'
    nicosia = 'Nicosia'
    prague = 'Prague'
    copenhagen = 'Copenhagen'
    tallinn = 'Tallinn'
    helsinki = 'Helsinki'
    paris = 'Paris'
    berlin = 'Berlin'
    athens = 'Athens'
    budapest = 'Budapest'
    dublin = 'Dublin'
    rome = 'Rome'
    riga = 'Riga'
    vilnius = 'Vilnius'
    luxembourg = 'Luxembourg'
    valleta = 'Valleta'
    amsterdam = 'Amsterdam'
    warsaw = 'Warsaw'
    lisbon = 'Lisbon'
    bucharest = 'Bucharest'
    bratislava = 'Bratislava'
    ljubljana = 'Ljubljana'
    madrid = 'Madrid'
    stockholm = 'Stockholm'


class WeatherData(BaseModel):
    city: str = Field(
        description='City', example='Vienna',
    )
    measure_date: Optional[datetime] = Field(
        None, description='Period', example='2021-07-21T17:32:28Z',
    )
    temperature: Optional[confloat(ge=-273.15, le=100.0)] = Field(
        None, description='Temperature Cel', example=35.5,
    )
    pressure: Optional[confloat(ge=0)] = Field(
        None, description='Pressure HPA', example=1058.0,
    )
    humidity: Optional[confloat(ge=0, le=100.0)] = Field(
        None, description='Humidity in percents', example=63.0,
    )
    cloudiness: Optional[confloat(ge=0, le=100.0)] = Field(
        None, description='Cloudiness oktas', example=4,
    )
    wind: Optional[confloat(ge=0)] = Field(None, description='Wind m/s', example=12.5)


class Error(BaseModel):
    error: Optional[str] = None
    error_description: Optional[str] = None


class Aggregations(Enum):
    median = 'avg'
    highest = 'max'
    lowest = 'min'


class ApiV1HistoricalDataCapitalGetResponse(BaseModel):
    limit: Optional[int] = Field(
        None, description='Rows limit per response', example=1000,
    )
    cursor: Optional[float] = Field(
        None, description='Cursor', example=12345635877.11244,
    )
    from_date: Optional[datetime] = Field(
        None, description='From period', example='2021-01-01',
    )
    till_date: Optional[datetime] = Field(
        None, description='Till period', example='2021-02-01',
    )
    aggregation: Optional[str] = Field(
        None, description='Aggregation type', example='median',
    )
    target: Optional[str] = Field(
        None, description='Target value to agreate', example='pressure',
    )
    results: Optional[List[WeatherData]] = []

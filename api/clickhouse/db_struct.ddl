CREATE DATABASE IF NOT EXISTS db_weather;

CREATE TABLE IF NOT EXISTS db_weather.facts(
    city               String,
    measure_date       Datetime,
    temperature      Nullable(Float32),
    pressure      Nullable(Float32),
    humidity        Nullable(Float32),
    cloudiness      Nullable(Float32),
    wind       Nullable(Float32)
) ENGINE = Log;
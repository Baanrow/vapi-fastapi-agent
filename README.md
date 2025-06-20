# vapi-fastapi-weather-tool

Modular FastAPI backend for handling Vapi voice tool calls and returning real-time weather data. Built to parse structured JSON, call the OpenWeather API, and format a tool-compatible response for voice-enabled agents.

This project provides a lightweight, scalable base for voice-to-API workflows. It’s designed to be tool-agnostic and can be extended to support additional endpoints, services, or tool schemas.

---

## 🌤️ What It Does

- Accepts a POST request from a Vapi voice assistant tool
- Extracts a city name from structured tool call arguments
- Queries OpenWeather for current temperature in Celsius
- Formats and returns the response in Vapi-compatible format
- Handles common error cases like invalid cities or missing data

---

## 🗂 File Structure

| File              | Purpose                                                              |
|-------------------|----------------------------------------------------------------------|
| `app.py`          | Main FastAPI app including `/api` endpoint and core logic            |
| `config.py`       | Environment variables for API key and base URL (not included)        |
| `models.py`       | Typed request and response models using Pydantic                     |

---

## 🔧 Tools & Technologies

- **FastAPI** – async-friendly Python web framework
- **httpx** – asynchronous HTTP client for external APIs
- **Pydantic** – data validation and parsing for nested inputs
- **OpenWeather API** – live weather source for city-based queries
- **Vapi Tool Schema** – structured input/output format for voice tools

---

## 🚀 Example Use Case

A user says:

> “What’s the weather in Paris?”

→ Vapi tool triggers POST to this FastAPI backend  
→ Backend fetches weather for Paris via OpenWeather  
→ Returns:  
`"The weather in Paris is a nice 31 degrees Celsius."`

---

## 🧩 Notes

- Modular layout makes it easy to swap in new tools, APIs, or endpoints.
- Tool call format is compatible with any voice interface using structured JSON.
- Designed for reuse across voice agents, assistants, or webhook-based automation.

---

## 🙋 About

Created by Brett C. as part of an AI workflow automation portfolio. I build modular FastAPI agents that connect APIs to real-time interfaces using clean, extensible code patterns.

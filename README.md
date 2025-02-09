# Restack AI - Quickstart

This repository contains a quickstart for Restack.
It demonstrates how to set up a basic agent with tool call with a basic workflow and functions.

## Prerequisites

- Docker (for running Restack)
- Python 3.10 or higher

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
```

## Start python shell

If using uv:

```bash
uv venv && source .venv/bin/activate
```

If using pip:

```bash
python -m venv .venv && source .venv/bin/activate
```

## Install dependencies

If using uv:

```bash
uv sync
uv run dev
```

If using pip:

```bash
pip install -e .
python -c "from src.services import watch_services; watch_services()"
```

## Run agents


### Get Bearer token

Authenticate REST API requests with a Bearer token. Generate one by running the following command:

```bash
openssl rand -base64 32
```

The new token should be set in the environment variable:

```bash
export BEARER_TOKEN=your_token
```

Run this command to restart the Restack container with the Bearer token:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -e BEARER_TOKEN=your_token ghcr.io/restackio/restack:main
```

### from API

```bash
curl -X POST http://localhost:6233/api/agents/QGAgent \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "input": {},
    "schedule": null
  }'
```

expected output:

```json
{
  "agentId": "1a3e18b5-QGAgent",
  "runId": "04edf314-784d-4e39-8fb5-a7e083cf8feb"
}
```
This will be use to send events to the agent

### Ask the agent to correct the data example (message event)

```bash
curl -X PUT http://localhost:6233/api/agents/QGAgent/1a3e18b5-QGAgent/04edf314-784d-4e39-8fb5-a7e083cf8feb \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ZbxVRaRNlSCTSjSDGufAA+1AnfUtVcCd5wtuUWWB54g=" \
  -d '{
    "eventName": "message",
    "eventInput": {
      "content": {
        "data": {
          "id": 5,
          "net": null,
          "from_bus": null,
          "to_bus": "",
          "length_km": 10.5,
          "std_type": "",
          "name": "Updated Line Name",
          "index": null,
          "geodata": null,
          "df": 1.0,
          "parallel": 1,
          "in_service": true,
          "max_loading_percent": 100.0,
          "alpha": null,
          "temperature_degree_celsius": null
        },
        "table_name": "line"
      }
    }
  }'
```

### Confirmation event to update the database

```bash
curl -X PUT http://localhost:6233/api/agents/QGAgent/1a3e18b5-QGAgent/04edf314-784d-4e39-8fb5-a7e083cf8feb \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ZbxVRaRNlSCTSjSDGufAA+1AnfUtVcCd5wtuUWWB54g=" \
  -d '{
    "eventName": "confirmation",
    "eventInput": {}
  }'
```

## Deploy on Restack Cloud

To deploy the application on Restack, you can create an account at [https://console.restack.io](https://console.restack.io)

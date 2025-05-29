#! /usr/bin/env bash


# Start Bedrock Magma standalone, using uvicorn.
#   This is a development mode good for fast iterations but requires some adjustments to network connections
#   The Compose stack will still be running so you have Postgres and pgAdmin, but you will bypass the running
#   Bedrock container and connect to postgres from your locally-running Magma FastAPI app, started like this:

uvicorn magmastart:app --reload


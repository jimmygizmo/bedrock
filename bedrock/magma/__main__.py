import uvicorn


# This code in __main__.py allows you to start Magma using:
#   python -m magma

# You could also use this as you Docker entrypoint. This is here mainly as an example of options for startup.
# Bedrock uses magma_entrypoint.py and does not use this 'python -m magma' method, which uses unicorn, not guvicorn.


if __name__ == "__main__":
    uvicorn.run(
        "magma.main:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
        factory=False
    )


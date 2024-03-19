import os
from webapp.app import create_app


def web_server(*args, **kwargs):
    print("web_server", args, kwargs)
    return create_app()

if __name__ == "__main__":
    import uvicorn
    port = os.getenv("PORT", "8080")
    assert port.isdigit(), "PORT must be a number"
    uvicorn.run(
        "main:web_server", host="0.0.0.0", port=int(port), reload=True
    )
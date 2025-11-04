from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="PageOff MVP")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>PageOff</title></head>
        <body style="font-family: sans-serif; text-align: center; margin-top: 3rem;">
            <h1>Hello PageOff 🚀</h1>
            <p>The Flixchart for books — MVP booting up.</p>
        </body>
    </html>
    """

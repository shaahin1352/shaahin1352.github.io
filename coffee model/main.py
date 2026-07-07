from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pysd

app = FastAPI()

# پوشه‌های HTML و فایل‌های استاتیک
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# خواندن مدل
model = pysd.read_vensim("coffee.mdl")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/run")
def run_model(room_temp: float = 29, adjust: float = 30):

    print("Room Temp =", room_temp)
    print("Adjust =", adjust)

    result = model.run(
        params={
            "room temp": room_temp,
            "adjust": adjust
        }
    )

    return result.reset_index().to_dict(orient="records")
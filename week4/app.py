from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="random")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def handle_session(request: Request, call_next):
    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/square/{number}", response_class=HTMLResponse)
def calculator(request: Request, number: int):
    result = number ** 2
    return templates.TemplateResponse("calculator.html", {"request": request, "result": result})


@app.get("/member", response_class=HTMLResponse)
def get_success(request: Request):
    if not request.session.get('signin'):
        raise HTTPException(status_code=403, detail="尚未登錄")
    return templates.TemplateResponse("success.html", {"request": request})


@app.get("/error", response_class=HTMLResponse)
def get_failure(request: Request, message: str = None):
    return templates.TemplateResponse("failure.html", {"request": request, "message": message})


@app.post("/signin", response_class=RedirectResponse)
def sign_in(request: Request, username: str = Form(None), password: str = Form(None)):
    if not (username and password):
        return RedirectResponse("/error?message=請輸入帳號、密碼", status_code=302)
    if username == "test" and password == "test":
        request.session['signin'] = True
        return RedirectResponse("/member", status_code=302)
    return RedirectResponse("/error?message=帳號、或密碼輸入錯誤", status_code=302)


@app.get("/signout", response_class=RedirectResponse)
def sign_out(request: Request):
    request.session.pop('signin', None)
    return RedirectResponse("/", status_code=302)

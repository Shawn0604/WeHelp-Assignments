from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from config import Config
import mysql.connector

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=Config.SESSION_SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=Config.MYSQL_PASSWORD,
    database="website"
)
cursor = db.cursor()

@app.middleware("http")
async def handle_session(request: Request, call_next):
    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# @app.get("/square/{number}", response_class=HTMLResponse)
# def calculator(request: Request, number: int):
#     result = number ** 2
#     return templates.TemplateResponse("calculator.html", {"request": request, "result": result})


@app.get("/member", response_class=HTMLResponse)
def get_success(request: Request):
    if not request.session.get('signin'):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("success.html", {"request": request})



@app.get("/error", response_class=HTMLResponse)
def get_failure(request: Request, message: str = None):
    return templates.TemplateResponse("failure.html", {"request": request, "message": message})

@app.post("/signup")
def sign_up(request: Request, name: str = Form(), username: str = Form(), password: str = Form()):
    try:
        cursor.execute("SELECT * FROM member WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
            db.commit()
            print("User created successfully.")
        else:
            print("Username already exists.")
            return RedirectResponse("/error?message=帳號重複", status_code=303)
        return RedirectResponse("/", status_code=303)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        return RedirectResponse("/error?message=資料庫錯誤", status_code=303)


@app.post("/signin", response_class=RedirectResponse)
def sign_in(request: Request, username: str = Form(None), password: str = Form(None)):
    if not (username and password):
        return RedirectResponse("/error?message=請輸入帳號、密碼", status_code=302)

    cursor.execute("SELECT password FROM member WHERE username = %s", (username,))
    user_record = cursor.fetchone()
    if user_record and user_record[0] == password:
        request.session['signin'] = True
        return RedirectResponse("/member", status_code=302)
    
    return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=302)



@app.get("/signout", response_class=RedirectResponse)
def sign_out(request: Request):
    request.session.pop('signin', None)
    return RedirectResponse("/", status_code=302)

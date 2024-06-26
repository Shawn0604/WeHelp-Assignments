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


@app.get("/member", response_class=HTMLResponse)
def get_success(request: Request):
    if not request.session.get('signin'):
        return RedirectResponse(url="/", status_code=302)
    
    cursor.execute("""
        SELECT m.content, mb.name 
        FROM message m
        JOIN member mb ON m.member_id = mb.id
        ORDER BY m.time DESC
    """)
    messages = cursor.fetchall()
    return templates.TemplateResponse("success.html", {
        "request": request, 
        "name": request.session.get('NAME', '会员'), 
        "messages": messages
    })





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
    cursor.execute("SELECT id, name, username, password FROM member WHERE username = %s", (username,))
    user_record = cursor.fetchone()
    if user_record and user_record[3] == password:
        request.session['signin'] = True
        request.session['ID'] = user_record[0]  
        request.session['NAME'] = user_record[1] 
        request.session['USERNAME'] = user_record[2]  
        return RedirectResponse("/member", status_code=302)
    else:
        return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=302)

@app.get("/signout", response_class=RedirectResponse)
def sign_out(request: Request):
    request.session.pop('signin', None)
    return RedirectResponse("/", status_code=302)


@app.post("/createMessage")
async def create_message(request: Request, content: str = Form(...)):
    print("Session data:", request.session) 
    member_id = request.session.get('ID')
    # if not member_id:
    #     return RedirectResponse("/error?message=未登入系统", status_code=302)

    try:
        cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (member_id, content))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        return RedirectResponse(f"/error?message=資料庫錯誤：{err.msg}", status_code=303)

    return RedirectResponse("/member", status_code=303)






@app.post("/deleteMessage")
async def delete_message(request: Request, message_id: str = Form(...)):
    username = request.session.get('name')
    if not username:
        return RedirectResponse("/error?message=未登入系統", status_code=302)
    try:
        # 首先檢查留言是否屬於當前用戶
        cursor.execute("SELECT username FROM messages WHERE id = %s", (message_id,))
        message_owner = cursor.fetchone()
        if message_owner and message_owner[0] == username:
            cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
            db.commit()
        else:
            return RedirectResponse("/error?message=無權限刪除此留言", status_code=403)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        return RedirectResponse("/error?message=資料庫錯誤", status_code=303)
    return RedirectResponse("/member", status_code=303)

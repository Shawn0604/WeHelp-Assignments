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
    
    # 使用 JOIN 查询来获取 message 和对应的 member name
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

    # 修改SQL查询以同时获取密码、id、name 和 username
    cursor.execute("SELECT id, name, username, password FROM member WHERE username = %s", (username,))
    user_record = cursor.fetchone()

    # 检查用户记录是否存在并且密码匹配
    if user_record and user_record[3] == password:
        # 用户验证成功，设置会话变量
        request.session['signin'] = True
        request.session['ID'] = user_record[0]  # 保存用户的 ID
        request.session['NAME'] = user_record[1]  # 保存用户的名称
        request.session['USERNAME'] = user_record[2]  # 保存用户的用户名
        return RedirectResponse("/member", status_code=302)
    else:
        # 如果密码不匹配或用户不存在，重定向到错误页面
        return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=302)

# @app.post("/signin", response_class=RedirectResponse)
# def sign_in(request: Request, username: str = Form(None), password: str = Form(None)):
#     if not (username and password):
#         return RedirectResponse("/error?message=請輸入帳號、密碼", status_code=302)

#     cursor.execute("SELECT id, name, username, password FROM member WHERE username = %s", (username,))
#     user_record = cursor.fetchone()
#     if user_record and user_record[3] == password:
#         request.session['SIGNED-IN'] = True
#         request.session['ID'] = user_record[0]  # 用户的 ID
#         request.session['NAME'] = user_record[1]  # 用户的名称
#         request.session['USERNAME'] = user_record[2]  # 用户的用户名
#         return RedirectResponse("/member", status_code=302)
#     else:
#         return RedirectResponse("/error?message=账号或密码输入错误", status_code=302)

# @app.post("/signin")
# def sign_in(request: Request, username: str = Form(None), password: str = Form(None)):
#     # 查询数据库，检索用户记录
#     cursor.execute("SELECT id, name, username, password FROM member WHERE username = %s", (username,))
#     user_record = cursor.fetchone()

#     # 如果用户记录存在且密码匹配
#     if user_record and user_record[3] == password:
#         # 正确设置会话信息
#         request.session['SIGNED-IN'] = True
#         request.session['ID'] = user_record[0]  # 用户的 ID
#         request.session['NAME'] = user_record[1]  # 用户的名称
#         request.session['USERNAME'] = user_record[2]  # 用户的用户名
        
#         # 重定向到会员页面
#         return RedirectResponse("/member", status_code=302)
#     else:
#         # 如果密码不匹配或用户不存在，重定向到错误页面
#         return RedirectResponse("/error?message=账号或密码输入错误", status_code=302)






@app.get("/signout", response_class=RedirectResponse)
def sign_out(request: Request):
    request.session.pop('signin', None)
    return RedirectResponse("/", status_code=302)


# @app.post("/createMessage")
# async def create_message(request: Request, content: str = Form(...)):
#     # 直接使用 session 中的 'id'，无需再定义 username 变量
#     member_id = request.session.get('id')
#     if not member_id:
#         return RedirectResponse("/error?message=未登入系統", status_code=302)

#     try:
#         # 插入留言到数据库
#         cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (member_id, content))
#         db.commit()
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         db.rollback()  # 回滚事务以保持数据一致性
#         # 使用错误信息作为响应，这里使用了 err.msg 来获取错误详细信息
#         return RedirectResponse(f"/error?message=資料庫錯誤：{err.msg}", status_code=303)

#     # 如果一切顺利，重定向用户到会员页面，看到他们的留言已发布
#     return RedirectResponse("/member", status_code=303)
@app.post("/createMessage")
async def create_message(request: Request, content: str = Form(...)):
    print("Session data:", request.session)  # 调试输出会话中的所有数据
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

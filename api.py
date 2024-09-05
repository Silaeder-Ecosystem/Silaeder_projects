from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import parse
import re
import db
import auth0

app = FastAPI()

@app.get("/allowed_users", response_model=list)
async def get_users():
    users = parse.parse_csv()
    return users

@app.get("/allowed_user/", response_model=bool)
async def get_users(email):
    if not email:
        return False
    users = parse.parse_csv()
    return email.lower() in users

@app.get("/projects")
async def get_projects():
    return db.get_all_projects_for_api()

@app.get("/is_user_exists")
async def is_user_exists(username):
    return {'exists': auth0.check_user_is_exist(username)}

if __name__ == '__main__':
    import uvicorn
    origins = [
        "http://ilyastarcek.ru:11701",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host="0.0.0.0", port=11702)



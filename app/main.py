import uvicorn

from app.constructors.app_constructor import app_constructor

app = app_constructor()


if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", reload=True, port=8001)

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

#sql lite connection through tortoise
register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models":["models"]},
    generate_schemas=True,
    add_exception_handlers= True
)




@app.get("/")
def index():
    return {"message":"Hello World"}



from fastapi import FastAPI


app = FastAPI(title="Web Boilerplate")


@app.get("/")
async def read_root():
    return {"status": "ok"}




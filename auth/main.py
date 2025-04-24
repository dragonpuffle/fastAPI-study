from fastapi import FastAPI
from routes import router as router_auth


app = FastAPI()

print("App is being created")


@app.get("/debug")
async def debug():
    print("DEBUG HIT")
    return {"ok": True}


app.include_router(router_auth)
# uvicorn auth.main:app --reload

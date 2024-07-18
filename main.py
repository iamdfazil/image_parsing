from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from invoice.routes import router as open_ai_route
from invoice.auth import router as auth_route

app = FastAPI(title='Image_Parser', version='1.0.0')

app.include_router(auth_route, prefix="/api/V1/auth", tags=["Auth"])
app.include_router(open_ai_route, prefix="/api/V1/image_parser", tags=["Image Parser"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Status": "Alive"}

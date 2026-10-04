from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html

from app.core.database import Base, engine
from app.routers.task_router import router as task_router

from app.routers.user_router import router as user_router
from app.routers.product import router as product_router
from app.routers.cart import router as cart_router
from dotenv import load_dotenv

load_dotenv()

# ⚠️ Move this later in production (important)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My Shop",
    docs_url=None,
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(task_router)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)


@app.get("/")
def home():
    return {"message": "Fake Store API Running"}


@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Fake Store API Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/.well-known/appspecific/com.chrome.devtools.json")
def chrome_devtools():
    return JSONResponse({"status": "ok"})


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")

    return {"message": "Logged out successfully"}

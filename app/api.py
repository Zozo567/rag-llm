try:
    from app.configurations import API_PREFIX

    DOCS_URL = f'{API_PREFIX}/docs'
    OPENAPI_URL = f'{API_PREFIX}/openapi.json'
except ImportError as error:
    raise

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.apps.generator.controllers import generator_controller


app = FastAPI(
    docs_url=DOCS_URL,
    openapi_url=OPENAPI_URL
)


# @TODO: not for production
# @NOTE: original should be domain or IP of Client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health/check")
def health_check():
    return {"status": "healthy"}


app.include_router(
    generator_controller, prefix=f"{API_PREFIX}/generate", tags=["Generator"]
)

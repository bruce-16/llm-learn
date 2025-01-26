from fastapi import FastAPI
from pydantic import BaseModel
import logging

from server.get_web_content import GetWebContent

app = FastAPI()

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


class WebContentRequest(BaseModel):
    url: str


@app.post("/get_web_content")
async def get_web_content(request: WebContentRequest):
    get_web_content = GetWebContent()

    logging.info(f"Processing URL: {request.url}")

    try:
        result = await get_web_content.get_content(request.url)
        return result
    except Exception as e:
        logging.error(f"Error processing URL: {str(e)}")
        return {"error": str(e)}

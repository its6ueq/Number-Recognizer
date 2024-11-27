from typing import List

import base64
from fastapi import FastAPI, Request
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from numRecog import solveImage

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/upload")
async def upload_image(request: Request):
    try:
        print("Received image data") 
        body = await request.body()
        body_str = body.decode("utf-8")
        start_index = body_str.find("base64,") + len("base64,")
        end_index = body_str.find("\"}")
        image_data = body_str[start_index:end_index]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        image.save("received_image.png")
        return solveImage()
    except Exception as e:
        return {"error": str(e)}    
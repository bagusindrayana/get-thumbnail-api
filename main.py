from fastapi import FastAPI, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import base64
import os

import uvicorn

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get", status_code=200)
def get_cctv_cat(video_url: str, response=Response):
    cap = cv2.VideoCapture(video_url)
  
    if cap.isOpened() == False:
        print("!!! Unable to open URL")
        # read one frame
    
    ret, frame = cap.read()
    if ret == False:
        raise HTTPException(status_code=404, detail="Video not found")
    
    retval, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    cap.release()
    # return as image
    # response.headers["Content-Type"] = "image/jpeg"
    return Response(content=buffer.tobytes(), media_type="image/jpeg")


    # jpg_as_text = base64.b64encode(buffer)
    # return jpg_as_text

default_port = "8111"
try:
    port = int(float(os.getenv("PORT", default_port)))
except TypeError:
    port = int(default_port)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

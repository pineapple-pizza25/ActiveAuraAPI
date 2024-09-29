from fastapi import FastAPI, UploadFile, Depends, Request, Form, status, File
from fastapi.responses import JSONResponse, FileResponse
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel


cred = credentials.Certificate("./service-account.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI()

class PostData(BaseModel):
    userEmail: str
    date: str
    title: str
    body: str

@app.get("/")
def home():
    return {"MESSAGE": "Hello there" }


@app.post("/createPost")
def createPost(post_data: PostData):
    try:
        doc_ref = db.collection("posts")
        doc_ref.add({
            "user-email": post_data.userEmail,
            "Date": post_data.date,
            "title": post_data.title,
            "body": post_data.body
        })
        return {"message": "Post created successfully", "post_id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
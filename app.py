from fastapi import FastAPI, UploadFile, Depends, Request, Form, status, File
from fastapi.responses import JSONResponse, FileResponse
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("./service-account.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI()

@app.get("/")
def home():
    return {"MESSAGE": "Hello there" }


@app.post("/createPost")
def createPost(userEmail: str, date: str, title: str, body: str):
    doc_ref = db.collection("posts")
    doc_ref.add({"user-email" : userEmail,
                  "Date": date,
                  "title": title, 
                  "body": body})

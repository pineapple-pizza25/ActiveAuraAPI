from fastapi import FastAPI, UploadFile, Depends, Request, Form, status, File
from fastapi.responses import JSONResponse, FileResponse
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from onesignal_sdk.client import Client


ONESIGNAL_APP_ID = 'a6e16b69-2e5c-4b04-bf3d-1b491f6a6844'
ONESIGNAL_API_KEY = 'NjQyMTc5ZmQtZDMxNC00MjhjLTk4MmItMTU5ZjE5MzNiNTE3'


cred = credentials.Certificate("./service-account.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI()

class PostData(BaseModel):
    userEmail: str
    date: str
    title: str
    body: str

class PostWithImageData(BaseModel):
    userEmail: str
    date: str
    title: str
    body: str
    imageBitmap: str 


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
        client = Client(app_id=ONESIGNAL_APP_ID, rest_api_key=ONESIGNAL_API_KEY)

        notification_body = {
            'headings': {'en': post_data.title},
            'contents': {'en': post_data.body},
            'included_segments': ["All"]
        }

        client.send_notification(notification_body)
        return {"message": "Post created successfully", "post_id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/createPostWithImage")
async def createPost(post_data: PostWithImageData):
    try:
        image_data = post_data.imageBitmap

        doc_ref = db.collection("posts")
        post_ref = doc_ref.add({
            "user-email": post_data.userEmail,
            "Date": post_data.date,
            "title": post_data.title,
            "body": post_data.body,
            "image": post_data.imageBitmap   
        })

        client = Client(app_id=ONESIGNAL_APP_ID, rest_api_key=ONESIGNAL_API_KEY)

        notification_body = {
            'headings': {'en': post_data.title},
            'contents': {'en': post_data.body},
            'included_segments': ["All"]
        }

        client.send_notification(notification_body)

        return {"message": "Post created successfully", "post_id": post_ref.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getPosts")
def getPosts():
    docs = db.collection("posts").stream()

    posts = []
    for doc in docs:
        posts.append(doc.to_dict()) 
    
    return posts

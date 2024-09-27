from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import shutil
from functions import extract_text_from_pdf, summarize, rag
import os

# Simulated user database
fake_users_db = {
    "user@example.com": {
        "username": "atou",
        "full_name": "koffi atou",
        "hashed_password": "fakehashedpassword",  #
    }
}

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI instance
app = FastAPI()

# Pydantic models
class User(BaseModel):
    username: str
    full_name: str = None
    email: str
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

# Function to verify user credentials (mock implementation)
def fake_hash_password(password: str):
    return "fakehashed" + password

def verify_password(plain_password, hashed_password):
    return fake_hash_password(plain_password) == hashed_password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Token route for authentication
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

# Dependency for authenticated user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user(fake_users_db, token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Utility function to save the uploaded PDF file to a temporary location
def save_upload_file(uploaded_file: UploadFile, destination: str) -> str:
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return destination

# PDF processing routes
@app.post("/summarize/")
async def summarize_text(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF.")
    
    # Save the uploaded file
    pdf_path = f"temp_{file.filename}"
    save_upload_file(file, pdf_path)
    
    # Extract text and summarize
    text = extract_text_from_pdf(pdf_path=pdf_path)
    text_summary = summarize(text)
    
    # Clean up the temporary file
    os.remove(pdf_path)
    
    return {"summary": text_summary}

@app.post("/question/")
async def answer_question(question: str, file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF.")
    
    # Save the uploaded file
    pdf_path = f"temp_{file.filename}"
    save_upload_file(file, pdf_path)
    
    # Extract text and run the question-answer model
    context = extract_text_from_pdf(pdf_path=pdf_path)
    result = rag(question=question, context=context)
    
    # Clean up the temporary file
    os.remove(pdf_path)
    
    return {"question": result['question'], "answer": result['answer']}

# If you want to run the app directly, uncomment the following line
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

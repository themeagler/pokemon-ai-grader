from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import urllib.request

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globals
model = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), "psa_model.keras")
MODEL_URL = "https://raw.githubusercontent.com/themeagler/psa-pokemon-backend/main/api/psa_model.keras"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Model loader on app startup
@app.on_event("startup")
def load_or_download_model():
    global model
    print(f"Checking for model at {MODEL_PATH}")
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Downloading...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Download complete.")
    else:
        print("Model found. Skipping download.")
    model = load_model(MODEL_PATH)
    print("Model loaded successfully.")

# Define label classes
class_names = ["psa10", "psa8", "psa9"]

@app.post("/grade")
async def grade_card(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))

        return JSONResponse({
            "grade": predicted_class,
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

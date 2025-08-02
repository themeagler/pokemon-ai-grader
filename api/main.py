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
    allow_origins=["*"],  # Replace with frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model path and GitHub-hosted backup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "psa_model.keras")
MODEL_URL = "https://raw.githubusercontent.com/themeagler/psa-pokemon-backend/main/api/psa_model.keras"

# Download the model if it's missing
if not os.path.exists(MODEL_PATH):
    print("Model file not found locally. Attempting to download from GitHub...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Model download complete.")

# Now load the model
model = load_model(MODEL_PATH)

# Define label classes (must match training order)
class_names = ["psa10", "psa8", "psa9"]

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/grade")
async def grade_card(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Preprocess the image
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))

        return JSONResponse({
            "grade": predicted_class,
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)



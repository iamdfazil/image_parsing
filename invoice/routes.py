import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any
from invoice.GCvision import detect_features
from invoice.utils import *

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/V1/auth/login")

@AuthJWT.load_config
def get_config():
    return Settings()

@router.post("/detect-features", response_model=Dict[str, Any], responses={200: {"description": "Success"}, 400: {"description": "Bad Request"}, 406: {"description": "Not Acceptable"}, 500: {"description": "Internal Server Error"}})
async def detect_features_endpoint(
    file_type: str = Form(..., description="The expected type of the image: 'speedometer' or 'vehicle_exterior'"),
    file: UploadFile = File(..., description="The image file to be analyzed"),
    token: str = Depends(oauth2_scheme)
):
    try:
        logging.debug(f"Received file: {file.filename}")
        logging.debug(f"Expected file type: {file_type}")

        # Check if file is an image
        if not file.content_type.startswith('image'):
            logging.error(f"Uploaded file is not an image: {file.content_type}")
            raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

        # Save the uploaded file locally
        file_location = f"uploads/{file.filename}"
        with open(file_location, 'wb') as f:
            content = await file.read()
            f.write(content)

        logging.debug(f"File saved at: {file_location}")

        # Detect features using the function from GCvision.py
        detection_results = detect_features(file_location)

        if detection_results is None:
            logging.error("Detection results are None")
            raise HTTPException(status_code=500, detail="Detection failed")

        logging.debug(f"Detection results: {detection_results}")

        # Determine the status and response based on detection results and expected file type
        response_content = {
            "Status": 200,
            "information": {
                "message": "Detection completed.",
                "file_name": file.filename,
                "detection_results": {}
            }
        }

        if file_type.lower() == "speedometer" and detection_results["speedometer"]:
            response_content["information"]["detection_results"] = "Speedometer Image"
        elif file_type.lower() == "vehicle_exterior" and detection_results["vehicle_exterior"]:
            response_content["information"]["detection_results"] = {
                "vehicle_exterior": "Vehicle Exterior Image",
                "color": detection_results["color"]
            }
        else:
            # Return 406 Not Acceptable if the detected features do not match the expected file type
            return JSONResponse(status_code=406, content={
                "Status": 406,
                "information": {
                    "message": f"Not Acceptable: The uploaded image is not a {file_type}.",
                    "file_name": file.filename
                }
            })

        return JSONResponse(status_code=200, content=response_content)
    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        return JSONResponse(status_code=e.status_code, content={
            "Status": e.status_code,
            "information": {
                "message": e.detail,
                "file_name": file.filename if 'file' in locals() else None
            }
        })
    except Exception as e:
        logging.error(f"Error in detect_features_endpoint: {e}")
        return JSONResponse(status_code=500, content={
            "Status": 500,
            "information": {
                "message": "Internal Server Error",
                "file_name": file.filename if 'file' in locals() else None
            }
        })

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from services.ml_models import predict_fake_news, predict_scam_message
from services.phishing import analyze_url
from services.ocr import extract_text_from_image
from auth.auth_handler import get_current_user

router = APIRouter()


class TextInput(BaseModel):
    text: str


class UrlInput(BaseModel):
    url: str


@router.post("/detect-fake-news")
async def detect_fake_news_endpoint(
    input_data: TextInput,
    current_user: dict = Depends(get_current_user)
):
    """Analyze text for fake news. Requires authentication."""
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    result = predict_fake_news(input_data.text)
    return result


@router.post("/detect-scam")
async def detect_scam_endpoint(
    input_data: TextInput,
    current_user: dict = Depends(get_current_user)
):
    """Analyze text for scam patterns. Requires authentication."""
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    result = predict_scam_message(input_data.text)
    return result


@router.post("/detect-phishing")
async def detect_phishing_endpoint(
    input_data: UrlInput,
    current_user: dict = Depends(get_current_user)
):
    """Analyze a URL for phishing characteristics. Requires authentication."""
    if not input_data.url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty.")
    result = analyze_url(input_data.url)
    return result


@router.post("/analyze-screenshot")
async def analyze_screenshot_endpoint(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Extract text from image via OCR and analyze for scams. Requires authentication."""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")
    try:
        image_bytes = await file.read()
        extracted_text = extract_text_from_image(image_bytes)

        if not extracted_text.strip():
            return {
                "error": "No text detected in the image.",
                "text": extracted_text}

        scam_result = predict_scam_message(extracted_text)
        return {
            "text_extracted": extracted_text,
            "analysis": scam_result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {
                str(e)}")

import base64
import io
import json
from typing import Literal
import anthropic
from PIL import Image, ImageOps
from pydantic import BaseModel

MODEL = "claude-opus-5-5"
MAX_SIDE = 1568
NOT_VISIBLE = {"salt", "pepper", "black pepper", "oil", "olive oil", "water",
               "sugar", "vinegar", "cumin", "cinnamon", "vegetable broth", "soy sauce"}
CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}

class DetectedIngredient(BaseModel):
    name: str
    confidence: Literal["low", "medium", "high"]

class DetectionResult(BaseModel):
    ingredients: list[DetectedIngredient]

def build_vocabulary(recipes):
    names = set()
    for raw in recipes["normalized_ingredients"]:
        names.update(json.loads(raw))
    return sorted(names - NOT_VISIBLE)

def prepare_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8")

def filter_detections(detections, vocabulary, min_confidence="medium"):
    allowed = set(vocabulary)
    seen = set()
    results = []
    for d in detections:
        name = d.name.strip().lower()
        if (name in allowed and name not in seen and CONFIDENCE_RANK[d.confidence] >= CONFIDENCE_RANK[min_confidence]):
            seen.add(name)
            results.append(DetectedIngredient(name=name, confidence=d.confidence))
    return results

PROMPT = """You are identifying food ingredients in a photo for a recipe app.

Allowed ingredient names:
{vocab}

Rules:
- Only list ingredients you can actually see in the photo.
- Use names from the allowed list exactly as written. If you see a food that is
  not on the list, leave it out unless it is truly the same food as a listed name.
- Do not guess hidden ingredients (spices, oil, salt) just because recipes often use them.
- confidence: "high" = clearly visible and identifiable, "medium" = probably,
  "low" = unsure.
- If no food is visible, return an empty list."""

def detect_ingredients(image_bytes, vocabulary, client=None, min_confidence="medium"):
    client = client or anthropic.Anthropic()
    image_b64 = prepare_image(image_bytes)
    response = client.beta.messages.parse(
        model=MODEL,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image",
                 "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64}},
                {"type": "text", "text": PROMPT.format(vocab=", ".join(vocabulary))}
            ],
        }],
        output_format=DetectionResult,
    )
    if response.stop_reason == "refusal" or response.parsed_output is None:
        return []
    return filter_detections(response.parsed_output.ingredients, vocabulary, min_confidence)
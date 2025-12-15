import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import os
import sys
import re  # Added Regex for text cleaning
from datetime import datetime

# --- CONFIGURATION ---
POPPLER_PATH = None 
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def system_check():
    try:
        ver = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract found: v{ver}")
    except Exception:
        print("❌ Tesseract NOT found.")
        sys.exit(1)

def apply_gamma(image, gamma=1.0):
    """
    Darkens the mid-tones (faint ink).
    """
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def preprocess_final(image):
    """
    V7.0: Gamma + CLAHE (The 'V6' Engine that worked best).
    """
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array

    # Darken faint text
    darker_gray = apply_gamma(gray, gamma=0.6)

    # Fix shadows/curves with CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced_img = clahe.apply(darker_gray)
    
    return enhanced_img

def clean_text_artifacts(text):
    """
    The 'Mop Up' Crew. 
    Uses Regex to find common OCR misreads and fix them textually.
    """
    # FIX: The "False e" Bullet Point
    # Logic: If a line starts with 'e' followed by a space and a Capital Letter,
    # it's 99% likely a bullet point, not the word 'e'.
    # Regex Breakdown:
    # ^\s* -> Start of a line (ignoring indentation)
    # [eE]      -> The letter e or E
    # [\s\.]+   -> Followed by space or period
    # (?=[A-Z]) -> Lookahead: Only if the NEXT letter is Capital (Start of sentence)
    cleaned = re.sub(r'^\s*[eE][\s\.]+(?=[A-Z])', '- ', text, flags=re.MULTILINE)
    
    # Optional: Fix common pipe '|' misreads as 'I' or 'l' if needed later
    # cleaned = cleaned.replace('|', 'I') 
    
    return cleaned

def ocr_pipeline(pdf_path, output_folder):
    file_name = os.path.basename(pdf_path).split('.')[0]
    print(f"\nProcessing: {file_name}...")
    
    debug_folder = os.path.join(output_folder, "debug_images_final")
    os.makedirs(debug_folder, exist_ok=True)
    
    try:
        if POPPLER_PATH:
            pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
        else:
            pages = convert_from_path(pdf_path, dpi=300)
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return

    full_text = []
    
    # Header
    full_text.append(f"--- TRANSCRIPT: {file_name} | {datetime.now().strftime('%Y-%m-%d')} ---\n")

    # Config: OEM 3 (Default) + PSM 3 (Auto Layout)
    custom_config = r'--oem 3 --psm 3'

    for i, page in enumerate(pages):
        print(f"  - Page {i+1}...")
        
        # 1. Vision Cleanup
        clean_img = preprocess_final(page)
        cv2.imwrite(os.path.join(debug_folder, f"{file_name}_p{i+1}.png"), clean_img)
        
        # 2. Extract Text
        raw_text = pytesseract.image_to_string(clean_img, lang='eng', config=custom_config)
        
        # 3. Text Cleanup (The new layer)
        final_text = clean_text_artifacts(raw_text)
        
        full_text.append(f"\n[--- PAGE {i+1} ---]\n{final_text}\n")

    output_path = os.path.join(output_folder, f"{file_name}_transcript.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_text))
        
    print(f"✅ FINAL SUCCESS! Saved: {output_path}")

if __name__ == "__main__":
    system_check()
    os.makedirs("input_pdfs", exist_ok=True)
    os.makedirs("output_text", exist_ok=True)
    
    files = [f for f in os.listdir("input_pdfs") if f.endswith(".pdf")]
    for file in files:
        ocr_pipeline(os.path.join("input_pdfs", file), "output_text")
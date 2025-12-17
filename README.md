# Clean-Room OCR: Automated Legal Document Digitization Pipeline

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![LegalTech](https://img.shields.io/badge/Domain-Legal_Tech-red) ![Status](https://img.shields.io/badge/Status-Prototype-green)

### 🚀 The "Elevator Pitch"
A specialized Optical Character Recognition (OCR) pipeline designed to extract searchable text from "dead" legacy legal documents (scanned deeds, rent agreements, and case files) while preserving the integrity of the original evidence.

---

### ⚖️ The Legal Problem
In Real Estate and M&A Due Diligence, lawyers often review thousands of pages of scanned PDFs. These documents are "dead data"—they cannot be searched (Ctrl+F), indexed, or analyzed by AI. 

Standard OCR tools often fail on Indian legal documents due to:
* **Faint Ink:** Old typewriters and carbon copies.
* **Binding Shadows:** Text curving into the spine of scanned deed books.
* **Artifacts:** Dust specks and hole-punch marks confusing the AI.

Furthermore, under **Section 65B of the Indian Evidence Act**, the digital extraction process must be "auditable" and non-destructive to the primary evidence.

---

### 🛠️ The Technical Solution
This pipeline uses a **"Clean-Room" approach**:

1.  **Ingestion:** Converts PDF pages to high-resolution images (300 DPI).
2.  **Vision Pre-processing (OpenCV):** * **Gamma Correction:** Darkens faint typewriter ink without ruining the page background.
    * **CLAHE (Contrast Limited Adaptive Histogram Equalization):** Intelligently removes shadows from curved book bindings.
3.  **Extraction (Tesseract 5.0):** Uses LSTM Neural Networks to read the text.
4.  **Post-Processing (NLP):** Uses Regular Expressions (Regex) to clean common OCR artifacts (e.g., misreading bullet points `•` as `e`).
5.  **Audit:** Generates a timestamped transcript, strictly separating the "Searchable Text" from the "Original Image."

---

### 📂 Project Structure

```text
Legal_OCR_Project/
├── input_pdfs/          # Drop raw scanned PDFs here
├── output_text/         # Transcript results appear here
│   └── debug_images/    # (Audit) Visual log of how the computer "saw" the document
├── ocr_pipeline.py      # Main execution engine
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```
### ⚙️ How to Run

**Step 1: Install Prerequisites**
* **Python 3.x**: Ensure it is installed.
* **Tesseract OCR**: Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
    * *Critical:* During installation, copy the path (e.g., `C:\Program Files\Tesseract-OCR`).
    * Add this path to your System Environment Variables.
* **Poppler**: Download from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows).
    * Unzip and place it in `C:\Program Files`.
    * Add the `bin` folder to your System Environment Variables.

<br>

**Step 2: Install Libraries**
Open your VS Code terminal and run this command:

```bash
pip install pytesseract pdf2image opencv-python numpy
```

<br>

**Step 3: Run the Pipeline**
1.  Navigate to the `input_pdfs` folder inside the project.
2.  Paste your scanned PDF files into this folder.
3.  Open your terminal and run the following command:

```bash
python ocr_pipeline.py
```
4.  Once finished, check the `output_text` folder to see your clean transcripts.
---

### 🔬 Technical Challenges & Optimizations

**1. The "Book Warp" Problem**
* **🔴 Challenge:** Scanned legal journals often have deep shadows near the book spine, causing text to fade into blackness.
* **🟢 Solution:** Implemented **CLAHE (Contrast Limited Adaptive Histogram Equalization)**. This algorithm locally boosts contrast in dark regions without over-exposing the white paper.

<br>

**2. The "Faint Ink" Problem**
* **🔴 Challenge:** 1980s typewriter ink is often light gray, which Tesseract ignores as "noise."
* **🟢 Solution:** Applied **Gamma Correction (0.6)**. This mathematically shifts mid-tone gray pixels to black, solidifying the font characters.

<br>

**3. The "False Bullet" Glitch**
* **🔴 Challenge:** The OCR engine frequently misread circular bullet points (`•`) as the letter `e`, corrupting the data structure.
* **🟢 Solution:** Built a custom **Regex Post-Processor**. It detects lines starting with `e` followed by a capital letter and programmatically converts them back to bullet dashes.
---

### 🔮 Future Roadmap

- [ ] **Geometric Dewarping:** Integrate 3D-vision models to mathematically flatten curved pages before processing.
- [ ] **Named Entity Recognition (NER):** Connect the text output to an NLP model to automatically extract "Party Names," "Survey Numbers," and "Transaction Values."
- [ ] **Cloud Fallback:** Create a hybrid mode that attempts Tesseract first, but auto-switches to AWS Textract for handwritten documents.
<br>
<hr>

### 👨‍💻 About the Developer
Built by **Poorna Chand Ballarapu**, a dual-degree student bridging the gap between Law and Technology.
* **Law:** 3rd Year B.A. LL.B (Hons) at **NALSAR University of Law**.
* **Tech:** B.S. in Data Science & Applications at **IIT Madras**.
* **Focus:** Leveraging Computational Law and NLP to automate complex legal workflows in M&A and Finance.




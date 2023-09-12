import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_to_png(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Iterate through each page and convert it to PNG
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        image = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image_bytes = image.samples
        image_pil = Image.frombytes("RGB", [image.width, image.height], image_bytes)
        
        # Save the image as PNG
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        image_pil.save(image_path)
        
        # Perform OCR on the image
        text = pytesseract.image_to_string(image_path)
        with open(os.path.join(output_folder, f"page_{page_number + 1}.txt"), "w") as text_file:
            text_file.write(text)

    # Close the PDF file
    pdf_document.close()

if __name__ == "__main__":
    pdf_file_path = "PDF.pdf"  # Replace with your input PDF file path
    output_folder_path = "output_images"  # Replace with the desired output folder path
    
    pdf_to_png(pdf_file_path, output_folder_path)
    print("PDF to PNG conversion and OCR complete!")
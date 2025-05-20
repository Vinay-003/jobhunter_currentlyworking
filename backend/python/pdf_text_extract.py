# pdf_text_extract.py
# Searches PostgreSQL for PDF file path with user_id = 4 and extracts text

import psycopg2  # For PostgreSQL connection
import fitz  # PyMuPDF for PDF text extraction
import os  # For file path validation

# Database configuration
DB_CONFIG = {
    'user': 'postgres',        # Replace with your username 
    'host': 'localhost',       # Database host
    'dbname': 'kafka_resume',          # Replace with your database name
    'password': '2006',# Replace with your password
    'port': 5432               # Default PostgreSQL port
}

def get_file_path(user_id):
    """Fetch PDF file path from database for given user_id."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        query = "SELECT file_path FROM resumes WHERE user_id = %s AND is_latest = TRUE LIMIT 1"
        cur.execute(query, (user_id,))
        result = cur.fetchone()
        if result:
            print(f"File path found: {result[0]}")
            return result[0]
        print("No file path found for user_id =", user_id)
        return None
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def extract_pdf_text(pdf_path):
    """Extract all text from the PDF at the given path."""
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at: {pdf_path}")
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        print("Text extraction completed")
        return text
    except Exception as e:
        print(f"PDF error: {e}")
        return None

def main():
    """Main function to search for PDF path and extract text."""
    user_id = 4
    print(f"Searching for PDF file path for user_id = {user_id}")
    file_path = get_file_path(user_id)
    if file_path:
        text = extract_pdf_text(file_path)
        if text:
            print("Extracted text:")
            print(text)
        else:
            print("Failed to extract text")
    else:
        print("Failed to retrieve file path")

if __name__ == "__main__":
    main()
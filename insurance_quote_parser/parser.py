import os
import re
import glob
from pypdf import PdfReader
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_pdf_list() -> list:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Looking for PDF files in parent directory: {parent_dir}")

    # Get all files in the directory
    all_files = glob.glob(f"{parent_dir}/input/auto_quote_documents/*")

    # Use regex to filter for PDF files case-insensitively
    pdf_files = []
    for file in all_files:
        if re.search(r'\.pdf$', file, re.IGNORECASE):
            pdf_files.append(file)

    print(f"Found {len(pdf_files)} PDF files")
    return pdf_files

# Extract relevant text from pdfs
def extract_pdf_text(pdf_path: str) -> str:
    print(f"Extracting PDF text from {pdf_path}")

    reader = PdfReader(pdf_path)

    # printing number of pages in pdf file
    print(f'Number of pages: {len(reader.pages)}')

    # extracting all text from the pdf
    extracted_text = '\n'.join([page.extract_text() for page in reader.pages])

    print(f'Sample extracted text (First 20 characters): {extracted_text[:20]}')

    return extracted_text

# Get prompt
def get_prompt():
    prompt_path = f'{os.path.dirname(os.path.abspath(__file__))}/input/prompt/prompt.txt'
    with open(prompt_path, 'r') as f:
        prompt = f.read()
    return prompt


# Get output for each and store
def call_openai_extraction(document_text):
    full_prompt = (f"INSTRUCTIONS:\n{document_text}"
                   f"DOCUMENT:\n{document_text}")

    client =  OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response.choices[0].message['content']

def run():
    pdf_list = get_pdf_list()
    print(pdf_list)
    for pdf in pdf_list:
        pdf_text = extract_pdf_text(pdf)
        extracted_text = call_openai_extraction(pdf_text)
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/output/{pdf}.pdf', 'wb') as f:
            f.write(extracted_text)


if __name__ == "__main__":
    run()
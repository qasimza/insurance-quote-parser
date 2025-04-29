import os
import re
import glob
from pypdf import PdfReader
from openai import OpenAI
import json

OPENAI_API_KEY = "" # Should be in .env for production

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

    return extracted_text

# Get prompt
def get_prompt():
    prompt_path = f'{os.path.dirname(os.path.abspath(__file__))}/input/prompts/prompt.txt'
    with open(prompt_path, 'r') as f:
        prompt = f.read()
    return prompt


# Use Open AI gpt-4.1-mini to extract relevant information
def call_openai_extraction(document_text):
    system_prompt = get_prompt()

    full_prompt = (f'INSTRUCTIONS:"""\n{system_prompt}"""'
                   f'BUSINESS AUTO (BA) INSURANCE QUOTE DOCUMENT:"""\n{document_text}"""')

    client =  OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response.choices[0].message.content

# Iterate over all pdfs and get jsons
def run():
    pdf_list = get_pdf_list()

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)

    for pdf in pdf_list:
        pdf_name = os.path.splitext(os.path.basename(pdf))[0]
        print(f"Processing: {pdf_name}")

        pdf_text = extract_pdf_text(pdf)  # If you're using text-based flow
        extracted_text = call_openai_extraction(pdf_text)  # Should return a JSON string or dict

        try:
            # Parse if needed
            data = json.loads(extracted_text) if isinstance(extracted_text, str) else extracted_text
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for {pdf_name}. Skipping.")
            print(f"OPEN AI Response: {extracted_text}")
            continue

        output_path = os.path.join(output_dir, f"{pdf_name}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"Saved: {output_path}")

if __name__ == "__main__":
    run()
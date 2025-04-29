# Insurance Quote Parser
An LLM Service for Parsing Arbitrary Business Auto Insurance Quotes into a Consolidated Data Structure.

## Input 
Business Auto (BA) quote documents as pdfs. Text is extracted using the `pypdf` module and passed to openAI's `gpt-4.1-mini` model (selected for its cost, speed and accuracy).

## Output 
One json object per document written to `insurance_quote_parser/output` directory. Format specified below:
```json
{
  "liabilityInsuranceLimit": "<value>",
  "liabilityInsuranceSymbol": "<value>",
  "medicalPaymentsLimit": "<value>",
  "medicalPaymentsSymbol": "<value>",
  "uninsuredMotoristLimit": "<value>",
  "uninsuredMotoristSymbol": "<value>",
  "underinsuredMotoristLimit": "<value>",
  "underinsuredMotoristSymbol": "<value>",
  "personalInjuryProtectionLimit": "<value>",
  "personalInjuryProtectionSymbol": "<value>",
  "hiredAutoLimit": "<value>",
  "hiredAutoSymbol": "<value>",
  "nonOwnedAutoLiabilityLimit": "<value>",
  "nonOwnedAutoLiabilitySymbol": "<value>",
  "collisionLimit": "<value>",
  "collisionDeductible": "<value>",
  "comprehensiveLimit": "<value>",
  "comprehensiveDeductible": "<value>",
  "vehicleSchedule": [
    {
      "year": "<value>",
      "make": "<value>",
      "model": "<value>",
      "vin": "<value>",
      "vehiclePremium": "<value>",
      "vehicleCost": "<value>"
    }
    // ... more vehicles
  ],
  "driverSchedule": [
    {
      "fullName": "<value>",
      "dateOfBirth": "<value>",
      "licenseNumber": "<value>"
    },
    // ... more drivers
  ],
}
```

## Developer Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/qasimza/insurance-quote-parser.git
cd insurance-quote-parser
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate
```
### 3. Install Requirements
```bash
pip3 install -r requirements.txt
```
### 4. Add Your OpenAI API Key
Open `parser.py` and insert your OpenAI API key at the top of the file:
```bash
import openai
openai.api_key = "your_openai_api_key_here"
```
### 5. Run the Application
```bash
python3 insurance_quote_parser/parser.py
```
### 6. Output
Extracted JSON files will be saved to the `./output/` directory.

## Testing and Results

Given time constraints, the current implementation only validates whether the OpenAI-generated output is saved as a `.json` file.

### Planned Test Rubric (if time permitted)

| Test Case Description                                      | Pass Criteria                                                                 |
|-----------------------------------------------------------|-------------------------------------------------------------------------------|
| **1. JSON File Format**                                   | A `.json` file is successfully written for each PDF in the output directory. |
| **2. Presence of Required Keys**                          | All top-level keys and nested field keys are present in the output JSON.     |
| **3. Structural Integrity**                               | The JSON structure strictly matches the specified schema (e.g., no extra/missing nesting). |
| **4. Value Accuracy**                                     | Extracted values match the source PDF content exactly or with acceptable formatting normalization. |
| **5. Non-null Fields Where Expected**                     | Fields that should have values (e.g., vehicle make/model) are not empty or `null`, unless justifiably missing. |
| **6. Robustness to Layout Variation** (stretch goal)      | Application produces valid output even when the document structure varies across different carriers. |
| **7. Graceful Handling of Missing/Suppressed Data**       | Fields are marked as `null` or `"Information suppressed"` as needed, without breaking the structure. |
| **8. Multiple Entry Handling**                            | Lists like `vehicleSchedule[]` and `driverSchedule[]` contain all entries from the PDF. |

> Note that only test #1 is currently implemented as a `try-except` block in the `run()` function of `parser.py`. Others remain conceptual for future improvements.

## Prompt Design Decisions 
1. **Role Definition**: The prompt casts the model as an "expert data extraction assistant" to encourage structured, task-oriented output.

2. **Input Clarification**: Specifies that the input is extracted text (not raw PDF), simplifying the model’s responsibilities.

3. **Explicit Null Handling**: Standardizes how to handle missing (`"null"`) and suppressed (`"Information suppressed"`) values to ensure consistency.

4. **Terminology Flexibility**: Instructs the model to use contextual clues for matching varied insurance terms (e.g., “Bodily Injury Liability” → `liabilityInsurance`).

5. **Standardized Formatting**: Enforces consistent formats for currency, dates, and coverage limits to simplify downstream validation.

## References 

### OpenAI Prompt Engineering Guide 
https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api




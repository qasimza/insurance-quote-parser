# Insurance Quote Parser
An LLM Service for Parsing Arbitrary Business Auto Insurance Quotes into a Consolidated Data Structure.

## Input 
Business Auto (BA) quote documents.

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
Create venv
Install requirements 
Run application


## Testing and Results

## Design Decisions 
- Shortest possible prompt 
- Guardrails to prevent hallucinations 
- Output validation and testing






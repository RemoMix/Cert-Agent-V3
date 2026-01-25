import React, { useState } from 'react';
import { ChevronDown, ChevronRight, FileText, AlertCircle, CheckCircle, Folder, Settings, Database, Printer, Search } from 'lucide-react';

const CertAgentDocs = () => {
  const [expandedSections, setExpandedSections] = useState({});
  const [selectedAgent, setSelectedAgent] = useState('overview');

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const agents = [
    { id: 'overview', name: 'System Overview', icon: FileText, color: 'blue' },
    { id: 'get_cert', name: 'GetCertAgent', icon: Search, color: 'green' },
    { id: 'extract_data', name: 'ExtractDataAgent', icon: Folder, color: 'purple' },
    { id: 'cert_number', name: 'CertNumberExtractAgent', icon: FileText, color: 'orange' },
    { id: 'product_name', name: 'ProductNameExtractAgent', icon: FileText, color: 'orange' },
    { id: 'lot_number', name: 'LotNumberExtractAgent', icon: FileText, color: 'orange' },
    { id: 'lot_size', name: 'LotSizeExtractAgent', icon: FileText, color: 'orange' },
    { id: 'analysis_result', name: 'AnalysisResultExtractAgent', icon: FileText, color: 'orange' },
    { id: 'erp_raw', name: 'ERPrawAgent', icon: Database, color: 'cyan' },
    { id: 'erp_mrl', name: 'ERPmrlAgent', icon: Database, color: 'cyan' },
    { id: 'evaluation', name: 'EvaluationAgent', icon: AlertCircle, color: 'yellow' },
    { id: 'annotate', name: 'AnnotateAgent', icon: FileText, color: 'pink' },
    { id: 'printing', name: 'PrintingAgent', icon: Printer, color: 'gray' },
  ];

  const agentDocs = {
    overview: {
      title: 'System Overview',
      description: 'Cert Agent V3 - Automated Certificate Processing System',
      sections: [
        {
          title: 'System Purpose',
          content: `
**Cert Agent V3** is an agent-based automation system designed to process laboratory certificate PDFs used in quality and compliance workflows in the herbs & spices industry.

**Core Philosophy:**
- This is a LEARNING and VALIDATION system, NOT a decision system
- Preserves extracted data exactly as recognized
- All evaluations are non-binding
- Requires human verification
- No automatic approval/rejection/blocking`,
        },
        {
          title: 'Design Principles',
          content: `
**1. OCR-First by Necessity**
- Certificates originate as paper documents
- PDFs produced via scanning
- Embedded PDF text is unreliable/non-existent
- System treats every certificate as image-based input

**2. Single Source of Truth**
- OCR executed once per page
- All downstream agents consume same OCR output
- No agent performs OCR independently

**3. Raw Data Preservation**
- Stored exactly as recognized
- Never corrected or normalized
- Never interpreted at extraction time

**4. Separation of Concerns**
- Each agent has ONE responsibility
- Does NOT perform work outside scope
- Produces explicit artifacts`,
        },
        {
          title: 'System Architecture',
          content: `
**Pipeline Flow:**

Email (Outlook)
    ↓
GetCertAgent (Download PDFs)
    ↓
ExtractDataAgent (OCR + Orchestration)
    ├─ CertNumberExtractAgent
    ├─ ProductNameExtractAgent
    ├─ LotNumberExtractAgent
    ├─ LotSizeExtractAgent
    └─ AnalysisResultExtractAgent
    ↓
ERPrawAgent (Supplier Lookup)
    ↓
ERPmrlAgent (MRL Lookup)
    ↓
EvaluationAgent (Compare & Flag)
    ↓
AnnotateAgent (Add Supplier Info)
    ↓
PrintingAgent (Print Certificate)`,
        },
        {
          title: 'Folder Structure',
          content: `
Cert_Agent_V3/
├── GetCertAgent/
│   └── Cert_Inbox/
├── ExtractDataAgent/
│   ├── Cert_To_PNG_OCR/
│   ├── Cert_Data_CSVs/
│   ├── CertNumberExtractAgent/Cert_Number_CSVs/
│   ├── ProductNameExtractAgent/Product_Name_CSVs/
│   ├── LotNumberExtractAgent/Lot_Number_CSVs/
│   ├── LotSizeExtractAgent/Lot_Size_CSVs/
│   └── AnalysisResultExtractAgent/Analysis_Result_CSVs/
├── ERPrawAgent/ERPraw_CSVs/
├── ERPmrlAgent/ERPmrl_CSVs/
├── EvaluationAgent/Evaluation_CSVs/
├── AnnotateAgent/Annotated_PDFs/
├── PrintingAgent/Final_PDFs/
├── Source_Data/
│   ├── Raw Warehouses.xlsx
│   ├── EU Limits Data.xlsx
│   ├── pesticides_list.csv
│   └── products_list.csv
└── Printed_Cert/`,
        }
      ]
    },
    get_cert: {
      title: 'GetCertAgent',
      description: 'Downloads certificate PDFs from Outlook emails',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Primary Function:**
- Connect to Microsoft Outlook
- Search Inbox for certificate emails
- Download attached PDF files

**Detailed Steps:**
1. Check if Outlook is available
2. If unavailable: wait until available
3. If available: connect to Outlook
4. Search Inbox with filters:
   - Sender: fdesk@aldahlia.com
   - Subject contains: "CERT" or "CER" (case-insensitive)
5. Download all PDF attachments from matching emails`,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
- None (operates directly on Outlook Inbox)

**Output:**
- PDF files downloaded from matching emails
- Saved to: Cert_Agent_V3/GetCertAgent/Cert_Inbox/
- Filename: {original_pdf_name}.pdf

**Example:**
Certificate_12345-Dokki.pdf`,
        },
        {
          title: 'Implementation Details',
          content: `
**Technology:**
- Uses pywin32 (win32com.client)
- COM interface to Outlook

**Code Structure:**
\`\`\`python
class GetCertAgent(BaseAgent):
    def connect_outlook(self):
        # Retry logic with timeout
        pass
    
    def search_emails(self):
        # Filter by sender and subject
        pass
    
    def download_attachments(self, emails):
        # Save PDFs to Cert_Inbox
        pass
\`\`\`

**Configuration:**
- OUTLOOK_SENDER = "fdesk@aldahlia.com"
- OUTLOOK_SUBJECT_KEYWORDS = ["CERT", "CER"]
- RETRY_DELAY = 30 seconds`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Parse PDF content
❌ Extract any data
❌ Make any business decisions
❌ Modify emails
❌ Delete emails
❌ Move emails to folders`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Scenario 1: Outlook Unavailable**
- Wait indefinitely until Outlook becomes available
- Log warning every 30 seconds
- Do not crash or exit

**Scenario 2: No Matching Emails**
- No action taken
- Exit without error
- Log "No new certificates found"

**Scenario 3: PDF Download Failure**
- Skip failed attachment
- Continue with remaining attachments
- Log error with email details

**Recovery:**
- Agent can be re-run safely
- Will re-process unprocessed emails
- No duplicate downloads (based on filename)`,
        }
      ]
    },
    extract_data: {
      title: 'ExtractDataAgent',
      description: 'Central orchestrator for OCR and data extraction',
      sections: [
        {
          title: 'Responsibility',
          content: `
**ExtractDataAgent is the CENTRAL SPINE of Cert Agent V3**

**Primary Functions:**
1. Convert certificate PDFs → images (one per page)
2. Perform OCR once per page
3. Produce shared OCR package for downstream agents
4. Coordinate extraction by invoking 5 sub-agents
5. Collect raw outputs from all sub-agents
6. Assemble final CSV with all extracted data per lot

**Sub-Agents Managed:**
- CertNumberExtractAgent
- ProductNameExtractAgent
- LotNumberExtractAgent
- LotSizeExtractAgent
- AnalysisResultExtractAgent`,
        },
        {
          title: 'Internal Processing Flow',
          content: `
**Step 1: PDF → Images**
- Convert each PDF page to PNG
- Preserve page order
- High resolution for OCR quality

**Step 2: OCR Execution**
- Run OCR on each image
- Extract text lines with indices
- Optional: bounding boxes for coordinates
- Store results in JSON format

**Step 3: OCR Package Creation**
Structure:
\`\`\`
Cert_To_PNG_OCR/
├── Certificate_12345_page_1.png
├── Certificate_12345_page_1_ocr.json
├── Certificate_12345_page_2.png
└── Certificate_12345_page_2_ocr.json
\`\`\`

**Step 4: Sub-Agent Invocation**
- Call each extraction agent sequentially
- Provide OCR Package path
- Wait for CSV output

**Step 5: Data Aggregation**
- Read all sub-agent CSVs
- Combine into single dataset
- Handle multi-lot scenarios`,
        },
        {
          title: 'OCR Package Contract',
          content: `
**JSON Structure:**
\`\`\`json
{
  "page_number": 1,
  "lines": [
    {
      "text": "Certificate Number: 12345-Dokki",
      "line_index": 0,
      "bbox": {
        "x": 100,
        "y": 50,
        "width": 200,
        "height": 20
      }
    },
    {
      "text": "Product Name: Basil",
      "line_index": 1,
      "bbox": {...}
    }
  ]
}
\`\`\`

**Contract Rules:**
- This is the ONLY interface sub-agents see
- No sub-agent performs OCR independently
- All consume same OCR output
- Ensures consistency across extractions`,
        },
        {
          title: 'Multi-Lot Handling',
          content: `
**Lot Number Formats:**

**Type 1: Single Lot**
- Input: "139385"
- Output: 1 CSV file

**Type 2: Explicit Multi-Lot (Slash)**
- Input: "139912/139913"
- Output: 2 CSV files (one per lot)

**Type 3: Explicit Multi-Lot (Dash)**
- Input: "139679-139680"
- Output: 2 CSV files (one per lot)

**Type 4: Implicit Multi-Lot**
- Input: "139865/2"
- Output: 1 CSV file (represents 2 lots)
- Note: Single ERP lookup for base lot

**Aggregation Logic:**
1. Parse lot_number_raw
2. Determine lot count and type
3. For explicit multi-lot:
   - Create separate CSV per lot
   - Duplicate analysis results for each
4. For implicit multi-lot:
   - Create single CSV
   - Add metadata field: lot_count`,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
1. PDF files from: Cert_Agent_V3/GetCertAgent/Cert_Inbox/
2. CSV outputs from sub-agents:
   - Cert_Number_CSVs/
   - Product_Name_CSVs/
   - Lot_Number_CSVs/
   - Lot_Size_CSVs/
   - Analysis_Result_CSVs/

**Output 1: OCR Package**
- Location: Cert_Agent_V3/ExtractDataAgent/Cert_To_PNG_OCR/
- Files per PDF:
  - {pdf_name}_page_X.png
  - {pdf_name}_page_X_ocr.json

**Output 2: Aggregated Data CSV**
- Location: Cert_Agent_V3/ExtractDataAgent/Cert_Data_CSVs/
- Filename: {pdf_name}_{lot_number}_Data.csv
- One CSV per lot per certificate

**CSV Structure:**
| cert_number_raw | product_name_raw | lot_number_raw | lot_size_raw | analyte_raw | result_raw | pesticide_count |
|-----------------|------------------|----------------|--------------|-------------|------------|-----------------|
| 12345-Dokki     | Basil           | 139385         | 5000 Kg      | Chlorpyrifos| 0.01       | 15              |`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Parse data meaning
❌ Access ERP files
❌ Perform extraction logic itself
❌ Interpret extracted values
❌ Decide business meaning
❌ Validate data correctness
❌ Correct OCR mistakes`,
        },
        {
          title: 'Failure Behavior',
          content: `
**OCR Failure on Page:**
- Mark page as unreadable
- Log page number and error
- Continue with remaining pages
- Pipeline does NOT stop

**Sub-Agent Output Missing:**
- Leave corresponding fields empty
- Log warning
- Continue aggregation
- Do NOT block pipeline

**PDF Conversion Failure:**
- Log error with PDF filename
- Skip that PDF
- Continue with next PDF
- Send notification to admin

**Recovery Strategy:**
- All operations are idempotent
- Re-running agent will overwrite previous outputs
- No partial state corruption`,
        }
      ]
    },
    cert_number: {
      title: 'CertNumberExtractAgent',
      description: 'Extracts certificate number from OCR data',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Single Purpose:**
Extract raw certificate number text from OCR package

**Expected Format:**
- Pattern: "XXXXXX-Dokki"
- Example: "12345-Dokki", "98765-Dokki"
- Always ends with "-Dokki"`,
        },
        {
          title: 'Extraction Logic',
          content: `
**Search Strategy:**
1. Search across ALL pages in OCR package
2. Look for anchor keywords:
   - "Certificate Number"
   - "Cert No"
   - "Cert Number"
3. Take nearest valid value after anchor
4. Validate format: digits + "-Dokki"

**Implementation:**
\`\`\`python
def extract_cert_number(ocr_package):
    for page in ocr_package:
        for i, line in enumerate(page['lines']):
            if 'certificate number' in line['text'].lower():
                # Check next few lines
                for j in range(i+1, min(i+5, len(page['lines']))):
                    candidate = page['lines'][j]['text']
                    if validate_cert_format(candidate):
                        return candidate
    return ""
\`\`\``,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
- OCR Package from: Cert_Agent_V3/ExtractDataAgent/Cert_To_PNG_OCR/
- Reads all *_ocr.json files for the certificate

**Output:**
- CSV file with one row and two columns
- Location: Cert_Agent_V3/CertNumberExtractAgent/Cert_Number_CSVs/
- Filename: {pdf_name}_CertNumber.csv

**CSV Structure:**
| cert_info | cert_number_raw |
|-----------|----------------|
| Certificate Number | 12345-Dokki |`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Parse certificate number meaning
❌ Validate against ERP
❌ Perform OCR itself
❌ Validate format beyond basic check
❌ Guess or infer missing values
❌ Correct OCR mistakes`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Certificate Number Not Found:**
- Set cert_number_raw = "" (empty)
- Log warning with PDF filename
- Do NOT crash or block
- Return empty CSV

**Multiple Certificate Numbers Found:**
- Take the first valid occurrence
- Log warning about multiple matches
- Continue processing`,
        }
      ]
    },
    product_name: {
      title: 'ProductNameExtractAgent',
      description: 'Extracts product name from OCR data',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Single Purpose:**
Extract raw product name text from OCR package

**Context:**
- Product names are in English
- Refer to herbs & spices (e.g., Basil, Oregano, Parsley)
- Reference list available: products_list.csv`,
        },
        {
          title: 'Extraction Logic',
          content: `
**Search Strategy:**
1. Search across ALL pages in OCR package
2. Prefer header section (top 30% of first page)
3. Look for anchor keywords:
   - "Product Name"
   - "Product"
   - "Sample"
4. Take nearest text after anchor
5. Optionally fuzzy match against products_list.csv

**Implementation:**
\`\`\`python
def extract_product_name(ocr_package, products_list):
    # Priority 1: Header section of page 1
    header_lines = ocr_package[0]['lines'][:10]
    for i, line in enumerate(header_lines):
        if 'product' in line['text'].lower():
            candidate = header_lines[i+1]['text']
            # Fuzzy match against products_list
            best_match = find_closest_match(candidate, products_list)
            return best_match if similarity > 0.8 else candidate
    
    # Priority 2: Search all pages
    # ...
\`\`\``,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
1. OCR Package from: Cert_Agent_V3/ExtractDataAgent/Cert_To_PNG_OCR/
2. Reference list: Cert_Agent_V3/Source_Data/products_list.csv

**Output:**
- CSV file with one row and two columns
- Location: Cert_Agent_V3/ProductNameExtractAgent/Product_Name_CSVs/
- Filename: {pdf_name}_ProductName.csv

**CSV Structure:**
| cert_info | product_name_raw |
|-----------|-----------------|
| Product Name | Basil |`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Parse product name meaning
❌ Access ERP for validation
❌ Perform OCR itself
❌ Auto-correct misspellings (except fuzzy match)
❌ Translate to Arabic
❌ Infer product from other context`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Product Name Not Found:**
- Set product_name_raw = "" (empty)
- Log warning with PDF filename
- Return empty CSV

**No Match in Products List:**
- Return OCR text as-is
- Log "Unknown product: {name}"
- Human review required`,
        }
      ]
    },
    lot_number: {
      title: 'LotNumberExtractAgent',
      description: 'Extracts lot number from OCR data',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Single Purpose:**
Extract raw lot number text from OCR package

**CRITICAL:**
This is the MOST COMPLEX extraction due to 10+ different lot number formats.
Extraction must preserve the FULL raw string without parsing.`,
        },
        {
          title: 'Lot Number Formats (10 Types)',
          content: `
**Format 1: Single Lot**
- Pattern: "139385"
- Meaning: 1 lot, 1 supplier

**Format 2: Explicit Multi-Lot (Slash)**
- Pattern: "139912/139913"
- Meaning: 2 lots, possibly 1 supplier OR 2 suppliers

**Format 3: Implicit Multi-Lot**
- Pattern: "139865/2"
- Meaning: 2 lots, 1 supplier (base lot + 1 more)

**Format 4: Implicit Multi-Lot (3 lots)**
- Pattern: "139865/3"
- Meaning: 3 lots, 1 supplier

**Format 5: Implicit Multi-Lot (5 lots)**
- Pattern: "139865/5"
- Meaning: 5 lots, 1 supplier

**Format 6: Explicit Multi-Lot (Dash)**
- Pattern: "139679-139680"
- Meaning: 2 lots, possibly 1 supplier OR 2 suppliers

**Format 7: Alphanumeric**
- Pattern: "SFP228"
- Meaning: 1 lot

**Format 8: Complex Numeric**
- Pattern: "163-31-03-39-2394"
- Meaning: 1 lot

**Format 9: Alphanumeric with Slash**
- Pattern: "DH956-TX/2025"
- Meaning: 1 lot

**Format 10: Standard 5-digit**
- Pattern: "91191"
- Meaning: 1 lot`,
        },
        {
          title: 'Extraction Logic',
          content: `
**Search Strategy:**
1. Search across ALL pages
2. Look for anchor: "Lot Number" or "Lot No"
3. Take complete text from next line
4. Do NOT parse or split
5. Return full raw string

**Implementation:**
\`\`\`python
def extract_lot_number(ocr_package):
    for page in ocr_package:
        for i, line in enumerate(page['lines']):
            if 'lot number' in line['text'].lower() or 'lot no' in line['text'].lower():
                # Return complete next line as-is
                if i + 1 < len(page['lines']):
                    return page['lines'][i+1]['text'].strip()
    return ""
\`\`\`

**Important:**
- Do NOT split "139912/139913" into separate values
- Do NOT parse "139865/2" 
- Parsing happens in ExtractDataAgent aggregation`,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
- OCR Package from: Cert_Agent_V3/ExtractDataAgent/Cert_To_PNG_OCR/

**Output:**
- CSV file with one row and two columns
- Location: Cert_Agent_V3/LotNumberExtractAgent/Lot_Number_CSVs/
- Filename: {pdf_name}_LotNumber.csv

**CSV Structure:**
| cert_info | lot_number_raw |
|-----------|----------------|
| Lot Number | 139912/139913 |

**Examples:**
| lot_number_raw |
|----------------|
| 139385 |
| 139912/139913 |
| 139865/2 |
| SFP228 |
| DH956-TX/2025 |`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Parse lot number meaning
❌ Split multi-lot strings
❌ Determine lot count
❌ Access ERP for validation
❌ Perform OCR itself
❌ Validate format
❌ Distinguish explicit vs implicit multi-lot`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Lot Number Not Found:**
- Set lot_number_raw = "" (empty)
- Log warning with PDF filename
- Return empty CSV
- Downstream agents will flag LOT_NOT_FOUND_IN_ERP`,
        }
      ]
    },
    lot_size: {
      title: 'LotSizeExtractAgent',
      description: 'Extracts lot size with unit from OCR data',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Single Purpose:**
Extract raw lot size text from OCR package

**Expected Format:**
- Value + Unit
- Example: "5000 Kg", "10000 Kg", "500 Kg"
- Unit is almost always "Kg"`,
        },
        {
          title: 'Extraction Logic',
          content: `
**Search Strategy:**
1. Search across ALL pages
2. Look for anchor: "Lot Size" or "Lot Weight"
3. Capture value + unit as complete text
4. Preserve spacing and formatting

**Implementation:**
\`\`\`python
def extract_lot_size(ocr_package):
    for page in ocr_package:
        for i, line in enumerate(page['lines']):
            if 'lot size' in line['text'].lower():
                if i + 1 < len(page['lines']):
                    # Get next line, expect format: "5000 Kg"
                    return page['lines'][i+1]['text'].strip()
    return ""
\`\`\``,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
- OCR Package from: Cert_Agent_V3/ExtractDataAgent/Cert_To_PNG_OCR/

**Output:**
- CSV file with one row and two columns
- Location: Cert_Agent_V3/LotSizeExtractAgent/Lot_Size_CSVs/
- Filename: {pdf_name}_LotSize.csv

**CSV Structure:**
| cert_info | lot_size_raw |
|-----------|--------------|
| Lot Size | 5000 Kg |`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Parse lot size to numeric value
❌ Convert units
❌ Validate reasonable ranges
❌ Access ERP
❌ Perform OCR itself`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Lot Size Not Found:**
- Set lot_size_raw = "" (empty)
- Log warning with PDF filename
- Return empty CSV`,
        }
      ]
    },
    analysis_result: {
      title: 'AnalysisResultExtractAgent',
      description: 'Extracts pesticide analysis results table from OCR data',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Single Purpose:**
Extract raw analysis result rows from OCR package

**Context:**
- This is a TABLE extraction (multiple rows)
- Each row contains: pesticide name + test result
- Table can span multiple pages
- Reference list available: pesticides_list.csv

**Critical Note:**
This agent is a RECORDER, not an ANALYZER`,
        },
        {
          title: 'Extraction Logic',
          content: `
**Search Strategy:**
1. Search across ALL pages
2. Detect table start with anchors:
   - "Results of analysis"
   - "Compound or microbe"
   - "Analyte"
3. Continue reading rows until:
   - Next section header appears
   - Page ends
   - Empty rows
4. Extract each row as: (analyte_raw, result_raw)

**Implementation:**
\`\`\`python
def extract_analysis_results(ocr_package, pesticides_list):
    results = []
    in_table = False
    
    for page in ocr_package:
        for line in page['lines']:
            # Detect table start
            if 'results of analysis' in line['text'].lower():
                in_table = True
                continue
            
            # Extract rows
            if in_table:
                # Parse line into analyte + result
                # Fuzzy match analyte against pesticides_list
                row = parse_table_row(line['text'], pesticides_list)
                if row:
                    results.append(row)
    
    return results
\`\`\`

**Fuzzy Matching:**
- OCR may misspell pesticide names
- Use fuzzy matching against pesticides_list.csv
- Threshold: 85% similarity
- If no match: keep OCR text as-is`,
        },
        {
          title: 'Result Value Formats',
          content: `
**Numeric Results:**
- "0.01", "0.001", "0.05"
- Usually in mg/kg

**Non-Numeric Results:**
- "LOQ" (Limit of Quantification)
- "ND" (Not Detected)
- "<0.01" (Below detection limit)
- "N/A"

**Important:**
- Do NOT convert non-numeric to numeric
- Preserve exactly as recognized
- Downstream EvaluationAgent will flag non-numeric`,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
1. OCR Package from: Cert_Agent_V3/ExtractDataAgent/Cert_To_PNG_OCR/
2. Reference list: Cert_Agent_V3/Source_Data/pesticides_list.csv

**Output:**
- CSV file with multiple rows
- Location: Cert_Agent_V3/AnalysisResultExtractAgent/Analysis_Result_CSVs/
- Filename: {pdf_name}_AnalysisResult.csv

**CSV Structure:**
| analyte_raw | result_raw |
|-------------|------------|
| Chlorpyrifos | 0.01 |
| Carbendazim | LOQ |
| Imidacloprid | 0.005 |
| Metalaxyl | ND |

**Empty Table:**
If no results found:
| analyte_raw | result_raw |
|-------------|------------|
| | |`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Parse analysis results meaning
❌ Convert results to numbers
❌ Compare with MRL limits
❌ Merge duplicate analytes
❌ Decide pass/fail
❌ Correct OCR mistakes (except fuzzy match)
❌ Drop suspicious rows
❌ Access ERP
❌ Perform OCR itself`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Table Anchor Not Found:**
- Output CSV with empty rows
- Log warning

**OCR Page Unreadable:**
- Skip that page
- Log page number
- Continue with remaining pages

**Partial Table Extracted:**
- Output partial data
- Do NOT block pipeline
- Log "Incomplete table extraction"

**No Match in Pesticides List:**
- Keep OCR text as-is
- Log "Unknown pesticide: {name}"
- Human review will validate`,
        }
      ]
    },
    erp_raw: {
      title: 'ERPrawAgent',
      description: 'Looks up supplier and internal lot number from ERP',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Primary Function:**
Use extracted lot number to search in ERP file and retrieve:
- Internal lot number (company's internal tracking ID)
- Supplier name (in Arabic)

**Data Source:**
- File: Raw Warehouses.xlsx
- Structure: Multi-sheet Excel workbook
- Must search ALL sheets`,
        },
        {
          title: 'ERP File Structure',
          content: `
**Raw Warehouses.xlsx:**
- Column 1: Lot Number (external/certificate lot number)
- Column 3: Internal Lot Number
- Column 4: Supplier Name (Arabic text)

**Example:**
| Lot Number | ... | Internal Lot | Supplier Name |
|------------|-----|--------------|---------------|
| 139385 | ... | 2601 | سعيد حمدي |
| 139912 | ... | 2601 | ماهر سعد |
| 139913 | ... | 2602 | ماهر سعد |

**Multi-Sheet Search:**
- File contains multiple sheets (one per time period)
- Must search ALL sheets sequentially
- Stop on first match`,
        },
        {
          title: 'Lookup Logic',
          content: `
**For Single Lot:**
- Input: "139385"
- Search: Exact match in Column 1
- Output: Internal Lot + Supplier

**For Multi-Lot (Explicit):**
- Input: "139912/139913"
- Parse: ["139912", "139913"]
- Search each separately
- Output: Two rows (may have different suppliers)

**Implementation:**
\`\`\`python
def lookup_lot(lot_number_raw, erp_file):
    # Parse lot number
    lot_numbers = parse_lot_number(lot_number_raw)
    
    results = []
    for lot in lot_numbers:
        # Search all sheets
        for sheet in erp_file.sheets:
            match = sheet[sheet['Column1'] == lot]
            if match:
                results.append({
                    'lot_number_raw': lot,
                    'internal_lot_number': match['Column3'],
                    'supplier_name': match['Column4']
                })
                break
    
    return results
\`\`\``,
        },
        {
          title: 'Multi-Lot Scenarios',
          content: `
**Scenario 1: Same Supplier**
- Input: "139912/139913"
- 139912 → ماهر سعد لوط 2601
- 139913 → ماهر سعد لوط 2602
- Annotation: "ماهر سعد لوط 2601 - لوط 2602"

**Scenario 2: Different Suppliers**
- Input: "139912/139913"
- 139912 → سعيد حمدي لوط 2601
- 139913 → ماهر سعد لوط 2611
- Annotation: "سعيد حمدي لوط 2601 - ماهر سعد لوط 2611"

**Scenario 3: One Not Found**
- Input: "139912/139913"
- 139912 → سعيد حمدي لوط 2601
- 139913 → NOT FOUND
- Annotation: "سعيد حمدي لوط 2601 - 139913 A/N"
  (A/N = Address Not found)`,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
1. CSV files from: Cert_Agent_V3/LotNumberExtractAgent/Lot_Number_CSVs/
2. ERP file: Cert_Agent_V3/Source_Data/Raw Warehouses.xlsx

**Output:**
- CSV file (same structure with added columns)
- Location: Cert_Agent_V3/ERPrawAgent/ERPraw_CSVs/
- Filename: {pdf_name}_{lot_number}_ERPraw.csv

**CSV Structure:**
| cert_info | lot_number_raw | internal_lot_number | supplier_name |
|-----------|----------------|---------------------|---------------|
| Lot Number | 139385 | 2601 | سعيد حمدي |

**For Multi-Lot:**
| cert_info | lot_number_raw | internal_lot_number | supplier_name |
|-----------|----------------|---------------------|---------------|
| Lot Number | 139912 | 2601 | ماهر سعد |
| Lot Number | 139913 | 2602 | ماهر سعد |`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Decide supplier correctness
❌ Merge multiple suppliers
❌ Apply business rules
❌ Validate supplier names
❌ Translate Arabic to English
❌ Choose between conflicting suppliers`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Lot Not Found in ERP:**
- Leave internal_lot_number = "" (empty)
- Leave supplier_name = "" (empty)
- Log warning: "Lot {number} not found in ERP"
- Continue processing (no blocking)
- EvaluationAgent will flag: LOT_NOT_FOUND_IN_ERP

**Excel File Not Found:**
- Raise critical error
- Stop pipeline
- Admin notification required

**Excel File Corrupted:**
- Log error
- Try to continue with accessible sheets
- Flag incomplete lookup`,
        }
      ]
    },
    erp_mrl: {
      title: 'ERPmrlAgent',
      description: 'Looks up MRL limits for pesticides from ERP',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Primary Function:**
For each pesticide found in analysis results:
- Search for product in ERP MRL file
- Retrieve EU MRL limit for that pesticide-product combination

**Data Source:**
- File: EU Limits Data.xlsx
- Structure: Multi-sheet Excel workbook
- Each sheet = one product
- Rows = pesticides with MRL limits`,
        },
        {
          title: 'ERP MRL File Structure',
          content: `
**EU Limits Data.xlsx:**

**Sheet Names:**
- "Basil", "Oregano", "Parsley", etc.
- Sheet name = Product name

**Columns:**
- Column 1: Pesticide Name
- Column 2: EU MRL Limit (mg/kg)

**Example (Basil Sheet):**
| Pesticide | EU MRL |
|-----------|--------|
| Chlorpyrifos | 0.05 |
| Carbendazim | 0.1 |
| Imidacloprid | 0.05 |`,
        },
        {
          title: 'Lookup Logic',
          content: `
**Process:**
1. Read product_name_raw from ExtractDataAgent CSV
2. Find matching sheet in EU Limits Data.xlsx
3. For each analyte_raw:
   - Search pesticide name in sheet
   - Get EU MRL value
   - Add to output

**Implementation:**
\`\`\`python
def lookup_mrl(product_name, analytes, erp_mrl_file):
    # Find product sheet
    if product_name not in erp_mrl_file.sheet_names:
        print(f"Product '{product_name}' not found in MRL file")
        return None
    
    sheet = erp_mrl_file[product_name]
    results = []
    
    for analyte in analytes:
        # Search pesticide
        match = sheet[sheet['Pesticide'] == analyte]
        if match:
            eu_mrl = match['EU MRL'].values[0]
        else:
            print(f"Pesticide '{analyte}' not found for product '{product_name}'")
            eu_mrl = ""
        
        results.append({
            'analyte_raw': analyte,
            'eu_mrl': eu_mrl
        })
    
    return results
\`\`\``,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
1. CSV files from: Cert_Agent_V3/ExtractDataAgent/Cert_Data_CSVs/
2. ERP MRL file: Cert_Agent_V3/Source_Data/EU Limits Data.xlsx

**Output:**
- CSV file (same structure with added eu_mrl column)
- Location: Cert_Agent_V3/ERPmrlAgent/ERPmrl_CSVs/
- Filename: {pdf_name}_{lot_number}_ERPmrl.csv

**CSV Structure:**
| cert_number_raw | product_name_raw | lot_number_raw | lot_size_raw | analyte_raw | result_raw | pesticide_count | eu_mrl |
|-----------------|------------------|----------------|--------------|-------------|------------|-----------------|--------|
| 12345-Dokki | Basil | 139385 | 5000 Kg | Chlorpyrifos | 0.01 | 15 | 0.05 |
| 12345-Dokki | Basil | 139385 | 5000 Kg | Carbendazim | LOQ | 15 | 0.1 |`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Parse EU limits meaning
❌ Compare results with limits
❌ Decide pass/fail
❌ Validate MRL values
❌ Handle missing MRL
❌ Choose between multiple limits`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Product Not Found:**
- Print: "Product '{name}' not found in ERPmrl file"
- Leave ALL eu_mrl values empty for that certificate
- Continue processing
- EvaluationAgent will flag: MRL_NOT_FOUND

**Pesticide Not Found:**
- Print: "Pesticide '{name}' not found in ERPmrl file"
- Leave eu_mrl = "" for that pesticide only
- Continue with other pesticides
- EvaluationAgent will flag: MRL_NOT_FOUND

**Excel File Issues:**
- File not found → Critical error, stop pipeline
- Sheet corrupted → Log error, continue with accessible sheets
- Invalid MRL value → Keep as-is, flag in evaluation`,
        }
      ]
    },
    evaluation: {
      title: 'EvaluationAgent',
      description: 'Evaluates results against MRL limits',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Primary Function:**
Evaluate extracted laboratory results against ERP reference data

**CRITICAL:**
- Perform ONLY numeric and availability comparisons
- Generate evaluation report for manual review
- Do NOT make final decisions
- Do NOT approve/reject certificates

**This is an INFORMATIONAL agent, not a DECISION agent**`,
        },
        {
          title: 'Evaluation Rules',
          content: `
**Rule 1: ERP Lookup Check**
\`\`\`
IF internal_lot_number is empty:
    evaluation_flag = LOT_NOT_FOUND_IN_ERP
    evaluation_notes = "Lot number not found in Raw Warehouses"
\`\`\`

**Rule 2: Result Format Check**
\`\`\`
IF result_raw is NOT numeric (e.g., "LOQ", "ND", "<0.01"):
    evaluation_flag = RESULT_NOT_NUMERIC
    evaluation_notes = "Result cannot be compared (non-numeric value)"
\`\`\`

**Rule 3: MRL Availability Check**
\`\`\`
IF eu_mrl is empty for any analyte:
    evaluation_flag = MRL_NOT_FOUND
    evaluation_notes = "MRL limit not found for this pesticide-product combination"
\`\`\`

**Rule 4: Numeric Comparison**
\`\`\`
IF result_raw > eu_mrl:
    evaluation_flag = EXCEEDED
    evaluation_notes = "Result exceeds EU MRL limit"
ELSE:
    evaluation_flag = OK
    evaluation_notes = "Result within acceptable limits"
\`\`\``,
        },
        {
          title: 'Evaluation Flags',
          content: `
**Flag Types (Informational Only):**

**OK**
- Result is numeric
- MRL found
- Result ≤ MRL
- Action: None, informational only

**EXCEEDED**
- Result is numeric
- MRL found
- Result > MRL
- Action: Flag for human review

**MRL_NOT_FOUND**
- Product not in EU Limits Data, OR
- Pesticide not found for this product
- Action: Human must research MRL

**RESULT_NOT_NUMERIC**
- Result is "LOQ", "ND", "<0.01", etc.
- Cannot perform numeric comparison
- Action: Human interpretation required

**LOT_NOT_FOUND_IN_ERP**
- Lot number not in Raw Warehouses.xlsx
- Cannot verify supplier
- Action: Human must verify lot source

**INCOMPLETE_DATA**
- Required input CSV missing
- Unexpected error occurred
- Action: Check pipeline logs`,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
1. From ERPrawAgent: supplier_name, internal_lot_number
   - Location: Cert_Agent_V3/ERPrawAgent/ERPraw_CSVs/
2. From ERPmrlAgent: eu_mrl
   - Location: Cert_Agent_V3/ERPmrlAgent/ERPmrl_CSVs/
3. From ExtractDataAgent: lot_number_raw, product_name_raw, analyte_raw, result_raw
   - Location: Cert_Agent_V3/ExtractDataAgent/Cert_Data_CSVs/

**Output:**
- One CSV file per (certificate × lot)
- Location: Cert_Agent_V3/EvaluationAgent/Evaluation_CSVs/
- Filename: {pdf_name}_{lot_number}_Evaluation.csv

**CSV Structure:**
| cert_info | lot_number | supplier_name | internal_lot_number | analyte | result_raw | eu_mrl | evaluation_flag | evaluation_notes |
|-----------|------------|---------------|---------------------|---------|------------|--------|-----------------|------------------|
| Cert Info | 139385 | سعيد حمدي | 2601 | Chlorpyrifos | 0.01 | 0.05 | OK | Result within limits |
| Cert Info | 139385 | سعيد حمدي | 2601 | Carbendazim | 0.15 | 0.1 | EXCEEDED | Result exceeds limit |
| Cert Info | 139385 | سعيد حمدي | 2601 | Metalaxyl | LOQ | 0.05 | RESULT_NOT_NUMERIC | Cannot compare |`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Decide ACCEPT / REJECT / REVIEW
❌ Block printing or annotation
❌ Modify certificate PDFs
❌ Interpret business or regulatory meaning
❌ Auto-correct or guess values
❌ Make final compliance decisions
❌ Send approval notifications
❌ Update ERP systems`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Required Input CSV Missing:**
- Generate evaluation CSV with:
  - evaluation_flag = INCOMPLETE_DATA
  - evaluation_notes = "Missing: {csv_name}"
- Log error
- Continue pipeline

**Unexpected Error:**
- Generate evaluation CSV with error note
- Log full stack trace
- Continue pipeline (no blocking)
- Send admin notification

**Data Type Mismatch:**
- Handle gracefully
- Flag as RESULT_NOT_NUMERIC or MRL_NOT_FOUND
- Continue processing`,
        }
      ]
    },
    annotate: {
      title: 'AnnotateAgent',
      description: 'Annotates PDFs with supplier and lot information',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Primary Function:**
Annotate certificate PDFs with:
- Supplier name (in Arabic)
- Internal lot number(s)

**Annotation Location:**
- Top of first page
- Clearly visible
- Professional formatting`,
        },
        {
          title: 'Annotation Format',
          content: `
**Single Lot:**
\`\`\`
سعيد حمدي لوط 2601
\`\`\`

**Multi-Lot (Same Supplier):**
\`\`\`
ماهر سعد لوط 2601 - لوط 2602
\`\`\`

**Multi-Lot (Different Suppliers):**
\`\`\`
سعيد حمدي لوط 2601 - ماهر سعد لوط 2611
\`\`\`

**Lot Not Found:**
\`\`\`
سعيد حمدي لوط 2601 - 139913 A/N
\`\`\`
(A/N = Address Not found)`,
        },
        {
          title: 'Implementation Details',
          content: `
**Technology:**
- Library: PyPDF2 or reportlab
- Font: Arabic-compatible (e.g., Arial, Tahoma)
- Text direction: Right-to-left (RTL)

**Positioning:**
\`\`\`python
def annotate_pdf(pdf_path, supplier_info):
    # Open original PDF
    pdf = PdfReader(pdf_path)
    
    # Create annotation overlay
    annotation = create_text_overlay(
        text=supplier_info,
        position=(50, 750),  # Top-left corner
        font="Arial",
        font_size=14,
        color="red",
        direction="rtl"  # Right-to-left for Arabic
    )
    
    # Merge overlay with first page
    page = pdf.pages[0]
    page.merge_page(annotation)
    
    # Save annotated PDF
    output = PdfWriter()
    output.add_page(page)
    for i in range(1, len(pdf.pages)):
        output.add_page(pdf.pages[i])
    
    output.write(annotated_pdf_path)
\`\`\``,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
1. Original PDFs from: Cert_Agent_V3/GetCertAgent/Cert_Inbox/
2. Supplier data from: Cert_Agent_V3/ERPrawAgent/ERPraw_CSVs/

**Output:**
- Annotated PDF files
- Location: Cert_Agent_V3/AnnotateAgent/Annotated_PDFs/
- Filename: {pdf_name}_{lot_number}_Annotated.pdf

**For Multi-Lot:**
- If explicit multi-lot (different lots): Create separate PDF per lot
- If implicit multi-lot (e.g., /2): Single PDF with combined annotation`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Decide which supplier to use (if multiple)
❌ Handle multi-supplier conflict resolution
❌ Modify original PDF content
❌ Add evaluation results to PDF
❌ Add watermarks or stamps
❌ Change PDF structure`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Supplier Name Empty:**
- Annotate with: "Supplier Not Found"
- Log warning
- Continue processing

**PDF Corruption:**
- Skip that PDF
- Log error
- Continue with next PDF

**Arabic Font Missing:**
- Fallback to Unicode font
- Log warning
- Continue (may have rendering issues)

**Multiple Suppliers (Conflict):**
- Annotate all suppliers separated by " - "
- Log "Multiple suppliers found"
- Human review required`,
        }
      ]
    },
    printing: {
      title: 'PrintingAgent',
      description: 'Prints annotated certificates to physical printer',
      sections: [
        {
          title: 'Responsibility',
          content: `
**Primary Function:**
- Connect to local Windows printer
- Print annotated certificate PDFs
- Archive printed PDFs

**Printer:**
- Name: "HP Neverstop Laser 100x"
- Type: Local printer (USB or network)`,
        },
        {
          title: 'Printing Logic',
          content: `
**Process:**
1. Check printer availability
2. Queue PDF for printing
3. Wait for print job completion
4. Archive PDF to Printed_Cert folder
5. Log print status

**Implementation:**
\`\`\`python
import win32print
import win32api

def print_pdf(pdf_path, printer_name):
    # Check printer exists
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
    if printer_name not in [p[2] for p in printers]:
        raise PrinterNotFoundError()
    
    # Send to printer
    win32api.ShellExecute(
        0,
        "print",
        pdf_path,
        f'/d:"{printer_name}"',
        ".",
        0
    )
    
    # Wait for completion
    time.sleep(5)  # Adjust based on PDF size
    
    return True
\`\`\``,
        },
        {
          title: 'Input/Output',
          content: `
**Input:**
- Annotated PDFs from: Cert_Agent_V3/AnnotateAgent/Annotated_PDFs/

**Output:**
1. Physical printed certificates
2. Archived PDF files:
   - Location: Cert_Agent_V3/Printed_Cert/
   - Filename: {pdf_name}_{lot_number}_Printed.pdf
   - Purpose: Record of what was printed`,
        },
        {
          title: 'What It Does NOT Do',
          content: `
❌ Parse any data
❌ Access ERP
❌ Modify PDFs
❌ Decide what to print
❌ Choose printer dynamically
❌ Handle printer settings (duplex, color, etc.)`,
        },
        {
          title: 'Failure Behavior',
          content: `
**Printer Not Found:**
- Log error: "Printer 'HP Neverstop Laser 100x' not found"
- Retry every 30 seconds
- DO NOT crash or exit
- Wait for manual intervention (user turns on printer)

**Print Job Failure:**
- Log error with PDF filename
- Mark PDF as "print_failed"
- Continue with next PDF
- Admin notification

**Printer Offline:**
- Wait indefinitely with periodic retry
- Log status every minute
- Do NOT skip documents

**Paper Jam / Out of Paper:**
- Detected via printer status
- Pause until issue resolved
- Resume automatically when ready`,
        }
      ]
    },
  };

  const AgentIcon = ({ agent }) => {
    const AgentIconComponent = agent.icon;
    const colorClasses = {
      blue: 'bg-blue-100 text-blue-600',
      green: 'bg-green-100 text-green-600',
      purple: 'bg-purple-100 text-purple-600',
      orange: 'bg-orange-100 text-orange-600',
      cyan: 'bg-cyan-100 text-cyan-600',
      yellow: 'bg-yellow-100 text-yellow-600',
      pink: 'bg-pink-100 text-pink-600',
      gray: 'bg-gray-100 text-gray-600',
    };
    
    return (
      <div className={`p-2 rounded-lg ${colorClasses[agent.color]}`}>
        <AgentIconComponent className="w-5 h-5" />
      </div>
    );
  };

  const currentDoc = agentDocs[selectedAgent];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="flex h-screen">
        {/* Sidebar */}
        <div className="w-80 bg-white border-r border-slate-200 overflow-y-auto">
          <div className="p-6 border-b border-slate-200">
            <h1 className="text-2xl font-bold text-slate-800">Cert Agent V3</h1>
            <p className="text-sm text-slate-600 mt-1">Complete Documentation</p>
          </div>
          
          <div className="p-4">
            {agents.map((agent) => (
              <button
                key={agent.id}
                onClick={() => setSelectedAgent(agent.id)}
                className={`w-full flex items-center gap-3 p-3 rounded-lg mb-2 transition-all ${
                  selectedAgent === agent.id
                    ? 'bg-blue-50 border-2 border-blue-300'
                    : 'hover:bg-slate-50 border-2 border-transparent'
                }`}
              >
                <AgentIcon agent={agent} />
                <span className={`text-sm font-medium ${
                  selectedAgent === agent.id ? 'text-blue-700' : 'text-slate-700'
                }`}>
                  {agent.name}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-4xl mx-auto p-8">
            {/* Header */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 mb-6">
              <div className="flex items-center gap-4 mb-4">
                <AgentIcon agent={agents.find(a => a.id === selectedAgent)} />
                <div>
                  <h2 className="text-3xl font-bold text-slate-800">{currentDoc.title}</h2>
                  <p className="text-slate-600 mt-1">{currentDoc.description}</p>
                </div>
              </div>
            </div>

            {/* Sections */}
            {currentDoc.sections.map((section, idx) => (
              <div key={idx} className="bg-white rounded-xl shadow-sm border border-slate-200 mb-4 overflow-hidden">
                <button
                  onClick={() => toggleSection(`${selectedAgent}-${idx}`)}
                  className="w-full flex items-center justify-between p-6 hover:bg-slate-50 transition-colors"
                >
                  <h3 className="text-xl font-semibold text-slate-800">{section.title}</h3>
                  {expandedSections[`${selectedAgent}-${idx}`] ? (
                    <ChevronDown className="w-5 h-5 text-slate-400" />
                  ) : (
                    <ChevronRight className="w-5 h-5 text-slate-400" />
                  )}
                </button>
                
                {expandedSections[`${selectedAgent}-${idx}`] && (
                  <div className="px-6 pb-6 prose prose-slate max-w-none">
                    {section.content.split('\n').map((paragraph, pIdx) => {
                      if (!paragraph.trim()) return null;
                      
                      // Handle headers
                      if (paragraph.startsWith('**') && paragraph.endsWith('**')) {
                        return (
                          <h4 key={pIdx} className="text-lg font-semibold text-slate-800 mt-4 mb-2">
                            {paragraph.replace(/\*\*/g, '')}
                          </h4>
                        );
                      }
                      
                      // Handle code blocks
                      if (paragraph.startsWith('```')) {
                        return null; // Code blocks handled separately
                      }
                      
                      // Handle list items
                      if (paragraph.trim().startsWith('-') || paragraph.trim().startsWith('•')) {
                        return (
                          <li key={pIdx} className="text-slate-700 ml-6">
                            {paragraph.replace(/^[-•]\s*/, '')}
                          </li>
                        );
                      }
                      
                      // Handle cross marks
                      if (paragraph.trim().startsWith('❌')) {
                        return (
                          <div key={pIdx} className="flex items-start gap-2 text-red-600 my-1">
                            <span>❌</span>
                            <span>{paragraph.replace('❌', '').trim()}</span>
                          </div>
                        );
                      }
                      
                      // Handle check marks
                      if (paragraph.trim().startsWith('✅')) {
                        return (
                          <div key={pIdx} className="flex items-start gap-2 text-green-600 my-1">
                            <span>✅</span>
                            <span>{paragraph.replace('✅', '').trim()}</span>
                          </div>
                        );
                      }
                      
                      // Regular paragraphs
                      return (
                        <p key={pIdx} className="text-slate-700 leading-relaxed mb-3">
                          {paragraph}
                        </p>
                      );
                    })}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CertAgentDocs;
\# Sales Analytics System



\## Overview

This project is a Python-based Sales Data Analytics System built as part of an academic assignment.  

The system processes raw sales transaction data, cleans and validates it, performs analytical computations, integrates external API data, and generates a comprehensive business report.



The project demonstrates:

\- File handling and error handling

\- Data cleaning and validation

\- Data analysis using lists and dictionaries

\- API integration

\- Report generation in text format



---



\## Project Structure



sales-analytics-system/

│

├── main.py

├── README.md

├── requirements.txt

│

├── utils/

│ ├── file\_handler.py

│ ├── data\_processor.py

│ └── api\_handler.py

│

├── data/

│ ├── sales\_data.txt

│ └── enriched\_sales\_data.txt

│

└── output/

└── sales\_report.txt





---



\## Features Implemented



\### 1. Data File Handling \& Preprocessing

\- Reads non-UTF-8 encoded sales data files

\- Handles encoding issues gracefully

\- Removes empty lines and header row

\- Parses pipe-delimited records

\- Cleans commas in text and numeric fields

\- Validates transactions based on given rules



\### 2. Data Processing \& Analysis

\- Calculates total revenue

\- Region-wise sales analysis

\- Top selling products

\- Customer purchase analysis

\- Daily sales trend analysis

\- Peak sales day identification

\- Low performing products analysis



\### 3. API Integration

\- Fetches product data from DummyJSON API

\- Creates product ID to product information mapping

\- Enriches sales transactions with API data

\- Saves enriched data to a new file



\### 4. Report Generation

\- Generates a comprehensive text report including:

&nbsp; 1. Header \& metadata

&nbsp; 2. Overall summary

&nbsp; 3. Region-wise performance

&nbsp; 4. Top 5 products

&nbsp; 5. Top 5 customers

&nbsp; 6. Daily sales trend

&nbsp; 7. Product performance analysis

&nbsp; 8. API enrichment summary



The final report is saved to:

output/sales\_report.txt





---



\## How to Run the Project



1\. \*\*Install dependencies\*\*

```bash

pip install -r requirements.txt



2\. Run the analysis pipeline

Create a temporary runner or use an interactive Python session to:

a) Read and clean data

b) Enrich sales data

c) Generate the report



Example (already tested during development):



from utils.file\_handler import read\_sales\_data

from utils.data\_processor import parse\_transactions, enrich\_sales\_data

from utils.api\_handler import fetch\_all\_products, create\_product\_mapping

from main import generate\_sales\_report



raw\_lines = read\_sales\_data("data/sales\_data.txt")

transactions = parse\_transactions(raw\_lines)



api\_products = fetch\_all\_products()

product\_mapping = create\_product\_mapping(api\_products)



enriched\_transactions = enrich\_sales\_data(transactions, product\_mapping)



generate\_sales\_report(transactions, enriched\_transactions)





Notes \& Assumptions

1. The sales report file (sales\_report.txt) is overwritten on each run to ensure the report always reflects the latest analysis.

2\.  API enrichment depends on matching numeric Product IDs (e.g., P101 → 101). Products without matching API IDs are marked with API\_Match = False.

3\.  Some products cannot be enriched due to differences between the sales dataset and API catalog.

4\.  Minor data inconsistencies (e.g., negative or zero values) are handled strictly as per assignment validation rules.

5\.  The report generation function is intentionally placed in main.py as no separate file was specified in the assignment instructions.



Technologies Used

1. Python 3

2\. Requests library (for API integration)

3\. DummyJSON Products API

Project tested end-to-end before submission.
This repository follows the prescribed assignment structure.
All data processing steps were implemented as per instructions.
External API integration uses DummyJSON products API.
The generated report includes all required analytical sections.

## Assumptions












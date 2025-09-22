# Excel-test-App
A simple Django app to **upload**, **process**, and **download** Excel files.  
Can be tested using **Postman**.

## Setup Instructions

**Clone the repository**
   ```bash
   git clone https://github.com/your-username/Excel-test-App.git
   cd Excel-test-App
   ```
# -- API Endpoints (Postman Testing)

1. **Upload Excel**

URL: **POST** http://127.0.0.1:8000/upload/

Body → form-data → key = file, value = your Excel file

Expected Response: JSON response of columns

2. **Perform Operation**

URL: **POST** http://127.0.0.1:8000/operation/

Description: Runs a sample operation on the uploaded Excel file (add column/sum).

Expected Response: JSON data with results.

3. **Download Excel**

URL: **GET** http://127.0.0.1:8000/download/

Description: Downloads the processed Excel file.
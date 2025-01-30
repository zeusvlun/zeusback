# **zeusback: Wayback Machine Information Disclosure Scanner**

**zeusback** is a specialized tool designed to automate the process of finding potential information disclosure vulnerabilities in web applications by leveraging the Wayback Machine’s archive. The tool filters URLs for sensitive file extensions and fetches status codes to help identify exposed or sensitive data.

## **Features**

- **Wayback Machine Integration**: Automatically fetches archived URLs for a specified domain using the Wayback Machine.
- **File Extension Filtering**: Filters URLs based on file extensions commonly associated with sensitive data (e.g., `.xls`, `.pdf`, `.log`, `.db`, `.bak`, etc.).
- **Multi-threaded Scanning**: Uses a thread pool for faster status code retrieval.
- **Status Code Analysis**: Retrieves and displays HTTP status codes for the discovered URLs.
- **URL Export**: Option to save the filtered URLs to an output file for future analysis.
- **Interactive Banner**: Displays an aesthetic banner and prompts for user input for a seamless experience.

## **Prerequisites**

- **Python 3.x**
- **Required Python Packages**:
  - `colorama`
  - `requests`
  - `validators`

## **Installation**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/zeusvlun/zeusback.git
   cd zeusback
   ```

2. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

   Ensure `requirements.txt` contains:
   ```plaintext
   colorama
   requests
   validators
   ```

## **Usage**

1. **Run the tool:**

   ```bash
   python zeusback.py
   ```

2. **Enter the target URL**: When prompted, provide the URL of the target website (e.g., `https://example.com`).

3. **Validate and Process**:
   - The tool validates the URL for correctness.
   - Extracts the domain from the provided URL.

4. **Review Results**:
   - URLs are displayed alongside their HTTP status codes.
   - The tool also provides an option to save the results to `output.txt` for later review.

5. **Save Results (Optional):**
   - After the scan, choose whether to save the filtered URLs to a file.

## **Disclaimer**

- **Educational Purposes Only**: Zeusback is designed for educational, security research, and ethical penetration testing purposes only. Do not use this tool for illegal or malicious activities. Ensure you have explicit permission to scan the target domain.

## **Credits**

- **Wayback Machine** by [Internet Archive](http://wayback.archive.org/) – A powerful resource for retrieving and analyzing archived web content.

All tools are used under their respective open-source licenses.

## **Author**

**Created by:** [zeusvuln](https://x.com/ZeUsVuln/)


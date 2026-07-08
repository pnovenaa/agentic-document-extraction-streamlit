# Agentic Document Extraction Streamlit

An interactive **Streamlit** application for intelligent document extraction using **LandingAI ADE**. The application allows users to upload documents, extract structured information with AI, review extraction results, and export metadata in JSON format.

## Features

* 📄 Upload PDF and image documents
* 🤖 AI-powered document extraction using LandingAI ADE
* 📝 Display extracted text and structured fields
* 📚 View document references and supporting evidence
* 🏷️ Generate metadata in JSON format
* 💾 Download extraction results
* 🎨 Clean and user-friendly Streamlit interface

---

## Project Structure

```text
.
├── app.py                  # Main Streamlit application
├── services/
│   ├── extraction.py       # LandingAI extraction service
│   └── metadata.py         # Metadata generation
├── utils/
│   ├── helpers.py
│   └── schemas.py
├── assets/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/pnovenaa/agentic-document-extraction-streamlit.git
cd agentic-document-extraction-streamlit
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file (or configure Streamlit Secrets) with your LandingAI credentials.

Example:

```env
LANDINGAI_API_KEY=your_api_key
```

> **Note:** Never commit API keys or secrets to GitHub.

---

## Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default browser.

---

## Workflow

1. Upload a PDF or image document.
2. Submit the document for AI extraction.
3. Review the extracted content.
4. Inspect references and supporting evidence.
5. Generate structured metadata.
6. Download the output as JSON.

---

## Technologies

* Python
* Streamlit
* LandingAI ADE
* JSON Schema
* PDF Processing
* OCR & Document AI

---

## Example Use Cases

* Medical document extraction
* Insurance forms
* Financial statements
* Invoices
* Receipts
* Identity documents
* Custom document workflows

---

## Requirements

* Python 3.10+
* Streamlit
* LandingAI ADE SDK
* Additional dependencies listed in `requirements.txt`

---

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request for bug fixes, improvements, or new features.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Dependencies

Install the required packages manually:

```bash
pip install streamlit>=1.40.0 landingai python-dotenv landingai-ade
```

Or install them individually:

```bash
pip install streamlit>=1.40.0
pip install landingai
pip install python-dotenv
pip install landingai-ade
```

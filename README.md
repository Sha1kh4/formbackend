# Invoice Management Backend

This project is a FastAPI backend for uploading and managing invoices. It provides endpoints for uploading PDF invoices, storing metadata in a SQLite database, and listing all uploaded invoices.

## Features

*   Upload PDF invoices.
*   Store invoice metadata (client name, filename, upload date, source).
*   List all uploaded invoices.
*   CORS enabled for easy frontend integration.

## Technologies Used

*   [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   [SQLAlchemy](https://www.sqlalchemy.org/) - The Python SQL Toolkit and Object Relational Mapper.
*   [SQLite](https://www.sqlite.org/index.html) - A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
*   [Uvicorn](https://www.uvicorn.org/) - An ASGI server implementation, for running the FastAPI application.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Sha1kh4/formbackend.git
    cd formbackend
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r req.txt
    ```

4.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The application will be running at `http://127.0.0.1:8000`.

## API Endpoints

### `POST /upload`

Upload a new invoice.

**Parameters:**

*   `clientname` (string, form data): The name of the client.
*   `invoice` (file, form data): The PDF invoice file.
*   `source` (string, form data): The source of the invoice.

**Responses:**

*   `201 Created`: Invoice uploaded successfully.
    ```json
    {
      "message": "Invoice uploaded successfully",
      "invoice_id": 1
    }
    ```
*   `400 Bad Request`: If the uploaded file is not a PDF.

### `GET /invoices`

List all invoices.

**Responses:**

*   `200 OK`: A list of all invoices.
    ```json
    [
      {
        "id": 1,
        "clientname": "Test Client",
        "filename": "some-unique-filename.pdf",
        "uploaded_at": "2025-10-01T12:00:00",
        "source": "web"
      }
    ]
    ```

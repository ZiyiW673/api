# API File Reader

A simple Flask web application that lets you fetch files from an HTTP API using an API key and preview the response.

## Features

- Web form for supplying the API URL, API key, and header name.
- Sends the API key using the provided header (defaults to `Authorization: Bearer <key>`).
- Displays response metadata and renders a preview for text-based content types (JSON, XML, plain text, etc.).
- Handles request errors gracefully with user-friendly feedback.

## Requirements

- Python 3.10+

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the application

Start the Flask development server:

```bash
flask --app app run --debug
```

The site will be available at <http://127.0.0.1:5000/>.

## Usage

1. Enter the API URL that returns the file you want to read.
2. Provide the API key (if required).
3. Optionally customize the header name used for the key (defaults to `Authorization`).
4. Submit the form to fetch and preview the file response.

> **Note:** The application is intended for simple testing and development scenarios. Avoid using it to handle sensitive keys or large binary files in production environments.

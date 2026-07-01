# fileshares
Installation

    Clone the repository:
    bash

    git clone https://github.com/Jiks2217/fileshares.git
    cd fileshares

    Create and activate a virtual environment:
    bash

    python3.14 -m venv venv
    source venv/bin/activate

    Install dependencies:
    bash

    pip install -r requirements.txt

    Apply database migrations:
    bash

    python manage.py migrate

    Start the development server:
    bash

    python manage.py runserver

    Access the application at http://127.0.0.1:8000/

📌 Features

    Upload documents with metadata (name, email, description)

    Secure 12‑character alphanumeric access code generation

    Retrieve and download documents using the access code

    File type validation (PDF, Word, Excel, images, archives, etc.)

    Drag‑and‑drop file upload

    Copy access code to clipboard

🔒 Security Notes

    Files are stored in the media/ directory

    Access codes are generated cryptographically (secrets module)

    Never commit .env, local_settings.py, media/, or venv/ to version control

    Use environment variables for sensitive credentials in production




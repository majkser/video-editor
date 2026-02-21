# Video Editor Server

This is the backend server for the Video Editor project, built with FastAPI.

## Setup

1.  Create a virtual environment:

    ```bash
    python -m venv .venv
    ```

2.  Activate the virtual environment:
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Install ffmpeg on your system `https://www.ffmpeg.org/download.html`

## Running the Project

Run the server using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

You can access the API documentation at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`.

## Code Formatting

We use Black for code formatting.

**Format code before committing:**

To format all Python files in the current directory and its subdirectories, use:

```bash
black .
```

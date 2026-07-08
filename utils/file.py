from pathlib import Path


def save_uploaded_file(uploaded_file, upload_dir: Path) -> Path:
    """
    Save a Streamlit UploadedFile into upload_dir.

    Returns
    -------
    Path
        Saved file path.
    """

    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def ensure_directory(path: Path):
    """
    Create directory if it doesn't exist.
    """

    path.mkdir(parents=True, exist_ok=True)


def get_file_size_kb(file_path: Path) -> float:
    """
    File size in KB.
    """

    return round(file_path.stat().st_size / 1024, 2)
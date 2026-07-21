"""File type category definitions."""

CATEGORIES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
        ".ico", ".tiff", ".tif", ".psd", ".raw", ".heic", ".avif",
    ],
    "Documents": [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".odt", ".ods", ".odp", ".csv", ".tsv", ".rtf", ".tex",
    ],
    "Text": [
        ".txt", ".md", ".markdown", ".rst", ".asciidoc",
        ".log", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ],
    "Code": [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp",
        ".h", ".hpp", ".cs", ".rb", ".go", ".rs", ".swift", ".kt",
        ".scala", ".php", ".pl", ".lua", ".sh", ".bash", ".zsh",
        ".sql", ".r", ".m", ".mm",
    ],
    "Web": [
        ".html", ".htm", ".css", ".scss", ".sass", ".less",
        ".vue", ".svelte", ".ejs", ".hbs",
    ],
    "Archives": [
        ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
        ".iso", ".dmg", ".tgz",
    ],
    "Audio": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma",
        ".m4a", ".opus", ".mid", ".midi",
    ],
    "Video": [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv",
        ".webm", ".m4v", ".mpg", ".mpeg",
    ],
    "Data": [
        ".json", ".xml", ".csv", ".tsv", ".parquet", ".feather",
        ".hdf5", ".h5", ".pickle", ".pkl", ".db", ".sqlite",
        ".sqlite3",
    ],
    "Executables": [
        ".exe", ".msi", ".app", ".deb", ".rpm", ".dll", ".so",
        ".dylib", ".bin", ".sh", ".bat", ".cmd",
    ],
    "Fonts": [
        ".ttf", ".otf", ".woff", ".woff2", ".eot",
    ],
    "Design": [
        ".ai", ".eps", ".fig", ".sketch", ".xd",
    ],
}


def get_category(extension: str) -> str | None:
    """Return the category name for a given file extension."""
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return None

from httpx import Client

BASE_URL = "https://www.gutenberg.org/"


def create_client():
    return Client(base_url=BASE_URL, timeout=60.0, headers={"User-Agent": "Mozilla/5.0"})


def get_book_text(book_id: str) -> str:
    with create_client() as client:
        response = client.get(f"cache/epub/{book_id}/pg{book_id}.txt")
    if response.status_code == 404:
        raise Exception(f"No book with the id {book_id}")
    response.raise_for_status()
    return response.text

def download_book(book_id: str) -> str:
    with create_client() as client:
        response = client.get(f"cache/epub/{book_id}/pg{book_id}.txt")
    if response.status_code == 404:
        raise Exception(f"No book with the id {book_id}")
    response.raise_for_status()
    filename = f"books/livre{book_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)
    return f"downloaded as : {filename}"


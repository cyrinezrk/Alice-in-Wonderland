from httpx import Client

BASE_URL = "https://www.gutenberg.org/"


def create_client():
    return Client(base_url=BASE_URL)


def get_book_text(client: Client, book_id: str):
    response = client.get(f"cache/epub/{book_id}/pg{book_id}.txt")
    if response.status_code == 404:
        raise Exception(f"No book with the id {book_id}")
    response.raise_for_status()
    return response.text


def main():
    with create_client() as client:
        print(get_book_text(client, 45698453612))


if __name__ == "__main__":
    main()

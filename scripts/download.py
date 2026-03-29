import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://github.com/serengil/deepface_models/releases"

def get_h5_links():
    print("Fetching release page...")
    r = requests.get(BASE_URL)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    links = []
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href.endswith(".h5"):
            full_url = "https://github.com" + href
            links.append(full_url)

    return list(set(links))


def download_file(url):
    filename = url.split("/")[-1]
    print(f"Downloading {filename}...")

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"Saved: {filename}")


def main():
    links = get_h5_links()

    if not links:
        print("No .h5 files found ❌")
        return

    print(f"Found {len(links)} files")

    for link in links:
        download_file(link)


if __name__ == "__main__":
    main()
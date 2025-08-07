import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.lejebolig.dk/lejebolig"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

def fetch_lejeboliger(postnr, max_pages=1):
    results = []

    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}?page={page}&search=1&zip={postnr}"
        response = requests.get(url, headers=headers)

        # Hvis der er en fejl i forespørgslen, stop loopet
        if response.status_code != 200:
            print(f"Fejl ved forespørgsel til {url}: Statuskode {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "lxml")
        listings = soup.find_all("div", class_="listing-card")

        for listing in listings:
            try:
                title = listing.find("h2").get_text(strip=True)
                price = listing.find("div", class_="listing-card__price").get_text(strip=True)
                size = listing.find("div", class_="listing-card__size").get_text(strip=True)
                link = "https://www.lejebolig.dk" + listing.find("a")["href"]

                results.append({
                    "Titel": title,
                    "Pris": price,
                    "Størrelse": size,
                    "Link": link
                })
            except Exception:
                continue

    return pd.DataFrame(results)

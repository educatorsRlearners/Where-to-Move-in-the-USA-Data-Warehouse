from bs4 import BeautifulSoup
from itertools import chain
from typing import List, Optional
from constants import BASE_URL, BLANK, COMING_SOON, STORE_COLUMNS

import pandas as pd
import re
import requests


def get_contentbegin(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find(id="contentbegin")


def get_states(url: str) -> list[str]:
    results = get_contentbegin(url)
    if not results:
        return []
    states = [link.get("href") for link in results.find_all("a") if link.get("href")]
    return [BASE_URL + state for state in states]


def get_cities(url: str) -> list[str]:
    results = get_contentbegin(url)
    if not results:
        return []
    links = [link.get("href") for link in results.find_all("a") if link.get("href")]
    return links


def get_states_and_cities(url: str) -> list[str]:
    state_urls = get_states(url)
    cities = [get_cities(state) for state in state_urls]
    flat_cities = list(chain.from_iterable(cities))
    return [BASE_URL + city for city in flat_cities]


def get_store_urls(url: str) -> list[str]:
    results = get_contentbegin(url)
    if not results:
        return []
    links = [
        a.get("href")
        for a in results.find_all("a", {"data-linktrack": "Landing page"})
        if a.get("href")
    ]
    return [BASE_URL + link for link in links]


def get_full_store_urls(city_urls: list[str]) -> list[str]:
    store_urls = [get_store_urls(city) for city in city_urls]
    flat_store_urls = list(chain.from_iterable(store_urls))
    return list(set(flat_store_urls))


def get_all_store_urls() -> list[str]:
    city_urls = get_states_and_cities(BASE_URL)
    return get_full_store_urls(city_urls)


def _extract_store_name(data_galoc: Optional[str]) -> str:
    if not data_galoc or data_galoc == BLANK:
        return BLANK
    match = re.match(r"^(.+?\(\d+\))", data_galoc)
    return match.group(1) if match else BLANK


def _is_coming_soon(results: BeautifulSoup) -> bool:
    marker = results.find(class_="opening-comments-mobile") or results.find(
        class_="opening-comments"
    )
    return bool(marker and "Coming Soon" in marker.get_text(strip=True))


def _parse_address(results: BeautifulSoup) -> List[str]:
    div = results.find("div", class_="addressline")
    if not div:
        return [BLANK, BLANK, BLANK, BLANK]

    raw = div.get_text(separator="\n").replace("\t", "").replace(",", "").splitlines()
    cleaned = [line.strip() for line in raw if line.strip()]

    if len(cleaned) >= 4:
        street = cleaned[0]
        city = cleaned[1]
        state = cleaned[2]
        zip_code = cleaned[3]
        return [street, city, state, zip_code]

    return [BLANK, BLANK, BLANK, BLANK]


def _parse_phone_link(phone_link) -> str:
    if not phone_link:
        return BLANK
    href = phone_link.get("href")
    if not href or ":" not in href:
        return BLANK
    return href.split(":", 1)[1].strip()


def _extract_store_number(url: str) -> str:
    """Extract store number from URL like '/ca/el-cerrito/108/' → '108'"""
    return url.split("/")[-2]


def get_store_info(url: str) -> List[str]:
    results = get_contentbegin(url)
    if not results:
        return [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, url]

    address = _parse_address(results)
    store_number = _extract_store_number(url)

    if _is_coming_soon(results):
        return [store_number, COMING_SOON] + address + [COMING_SOON, url]

    phone_link = results.find("a", class_="ga_w2gi_lp phoneclr")
    store_name_raw = phone_link.get("data-galoc") if phone_link else None
    store_name = _extract_store_name(store_name_raw)
    phone_number = _parse_phone_link(phone_link)
    return [store_number, store_name] + address + [phone_number, url]


def write_store_urls_to_csv(urls_csv: str = "../data/store_urls.csv") -> list[str]:
    """Fetch all store URLs and write them to a CSV file"""
    all_store_urls = get_all_store_urls()

    urls_df = pd.DataFrame(all_store_urls, columns=["url"])
    urls_df.to_csv(urls_csv, index=False)

    print(f"Total store URLs: {len(all_store_urls)}")
    print(f"Store URLs written to {urls_csv}")

    return all_store_urls


def create_dataframe(
    urls_csv: str = "./data/store_urls.csv",
    output_csv: str = "./data/stores.csv",
    batch_size: int = 25,
) -> pd.DataFrame:
    """Read store URLs from CSV, process in batches, and write results to CSV"""
    # Read store URLs from CSV
    urls_df = pd.read_csv(urls_csv)
    all_store_urls = urls_df["url"].tolist()

    rows = []

    for batch_num, i in enumerate(range(0, len(all_store_urls), batch_size)):
        batch_urls = all_store_urls[i : i + batch_size]
        print(
            f"\nProcessing batch {batch_num + 1}: stores {i + 1} to {min(i + batch_size, len(all_store_urls))}"
        )

        batch_rows = [get_store_info(url) for url in batch_urls]
        rows.extend(batch_rows)

        # Write batch to CSV
        mode = "w" if i == 0 else "a"
        header = i == 0
        pd.DataFrame(batch_rows, columns=STORE_COLUMNS).to_csv(
            output_csv, mode=mode, header=header, index=False
        )
        print(f"Batch {batch_num + 1} written to {output_csv}")

    result_df = pd.DataFrame(rows, columns=STORE_COLUMNS)
    result_df["store_number"] = pd.to_numeric(result_df["store_number"], errors="coerce").astype("Int64")
    print(f"\nTotal stores processed: {len(result_df)}")
    print(f"All data written to {output_csv}")

    return result_df


if __name__ == "__main__":
    df = create_dataframe()

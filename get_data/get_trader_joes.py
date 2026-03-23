from bs4 import BeautifulSoup
from itertools import chain
from typing import List, Optional

import pandas as pd
import re
import requests

BLANK = "Blank"
COMING_SOON = "Coming Soon"


base_url = "https://locations.traderjoes.com"


def get_contentbegin(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="contentbegin")
    return results


def get_states(url):
    results = get_contentbegin(url)
    states = [link.get("href") for link in results.find_all("a")]
    state_urls = [base_url + state for state in states]  # type: ignore

    return state_urls


def get_cities(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="contentbegin")
    links = [link.get("href") for link in results.find_all("a")]
    return links


def get_states_and_cities(url):
    state_urls = get_states(url)
    # Creates a list of lists
    cities = [get_cities(state) for state in state_urls]

    # Flattens the list of lists to create a single list
    flat_cities = list(chain(*cities))

    city_urls = [base_url + city for city in flat_cities]  # type: ignore

    return city_urls


city_urls = get_states_and_cities(base_url)


def get_store_urls(url):

    results = get_contentbegin(url)

    links = [
        a.get("href") for a in results.find_all("a", {"data-linktrack": "Landing page"})  # type: ignore
    ]

    return [base_url + link for link in links]  # type: ignore


def get_full_store_urls(city_urls: list) -> list:
    store_urls = [get_store_urls(city) for city in city_urls]
    flat_store_urls = list(chain(*store_urls))
    all_store_urls = list(set(flat_store_urls))
    return all_store_urls


all_store_urls = get_full_store_urls(city_urls)


def _extract_store_name(data_galoc: Optional[str]) -> str:
    """Return store name like 'El Cerrito (108)' or BLANK."""
    if not data_galoc or data_galoc == BLANK:
        return BLANK
    m = re.match(r"^(.+?\(\d+\))", data_galoc)
    return m.group(1) if m else BLANK


def _is_coming_soon(results: BeautifulSoup) -> bool:
    """True if the page shows a 'Coming Soon' marker."""
    marker = results.find(class_="opening-comments-mobile") or results.find(
        class_="opening-comments"
    )
    return bool(marker and "Coming Soon" in marker.get_text(strip=True))


def _parse_address(results: BeautifulSoup) -> List[str]:
    """Return cleaned address lines (street, city/state, zip, …)."""
    div = results.find("div", class_="addressline")
    if not div:
        return [BLANK, BLANK]

    raw = div.get_text().replace("\t", "").replace(",", "").strip().splitlines()
    cleaned = [line.strip() for line in raw if line.strip()]
    return cleaned if cleaned else [BLANK, BLANK]


def _parse_phone_link(phone_link: Optional[object]) -> str:
    """Extract phone number from a phone <a> tag or return BLANK."""
    if not phone_link:
        return BLANK
    href = phone_link.get("href")
    if not href or ":" not in href:
        return BLANK
    parts = href.split(":", 1)
    return parts[1].strip() if len(parts) > 1 else BLANK


def get_store_info(url: str) -> List[str]:
    """Scrape a single Trader Joe’s location page and return:
    [store_name, addr1, addr2, …, phone, url]
    """
    results = get_contentbegin(url)

    # Fast path for "Coming Soon" stores
    if _is_coming_soon(results):  # type: ignore
        address = _parse_address(results)  # pyright: ignore[reportArgumentType]
        return [COMING_SOON] + address + [COMING_SOON] + [url]

    # Normal store: find the phone link once
    phone_link = results.find("a", class_="ga_w2gi_lp phoneclr")

    store_name_raw = phone_link.get("data-galoc") if phone_link else None
    store_name = _extract_store_name(store_name_raw)
    phone_number = _parse_phone_link(phone_link)
    address = _parse_address(results)

    return [store_name] + address + [phone_number] + [url]


def create_dataframe():
    store_info = [get_store_info(store) for store in all_store_urls]

    info = ["store_name", "street", "city", "state", "zip", "phone", "website"]

    return pd.DataFrame(store_info, columns=info)

import re
import time
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin
from config import USER_AGENT, TIMEOUT
from exceptions import FetchError
from core.models import Post


def create_session() -> object:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def fetch_page(session: object, url: str) -> str:
    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.RequestException as e:
        raise FetchError(f"Error fetching: {e}")


def parse_posts(html: str) -> list[object] | list[None]:
    soup = BeautifulSoup(html, "lxml")
    posts = []

    for i, row in enumerate(soup.select("tr.athing"), start=1):
        title_tag = row.select_one(".titleline a")
        if title_tag is None:
            continue

        title = title_tag.text.strip()
        url = title_tag.get("href")

        subtext_row = row.find_next_sibling("tr")
        subtext = subtext_row.select_one(".subtext") if subtext_row else None

        score_tag = subtext.select_one(".score") if subtext else None
        points = int(score_tag.text.replace(" points", "")) if score_tag else 0

        comments = 0
        link = subtext.select("a")[-1] if subtext else None
        if link:
            match = re.search(r"(\d+)\s*comment", link.text)
            comments = int(match.group(1)) if match else 0

        posts.append(Post(i, title, url, points, comments))

    return posts


def scrape_multiple_pages(
    session: object, start_url: str, max_pages: int = 3, delay: int = 2
) -> list[object] | list[None]:
    url = start_url
    posts = []
    post_count = 1
    page_count = 0

    while url and page_count < max_pages:
        try:
            html = fetch_page(session, url)
        except FetchError as e:
            print(f"  ⚠️  Stopped at page {page_count + 1}: {e}")
            break

        for post in parse_posts(html):
            post.rank = post_count
            posts.append(post)
            post_count += 1

        soup = BeautifulSoup(html, "lxml")
        more_link = soup.select_one(".morelink")
        url = urljoin(url, more_link["href"]) if more_link else None

        page_count += 1
        time.sleep(delay)

    return posts

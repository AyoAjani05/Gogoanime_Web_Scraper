from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_episode_links_from_first_page(url, browser_type="firefox"):
    """Scrapes episode links for the given anime URL using Playwright and BeautifulSoup.

    Args:
        url (str): The URL of the anime page on gogoanimes.fi.
        browser_type (str, optional): The Playwright browser type to use ('firefox' by default).

    Returns:
        list: A list of episode links.
    """

    with sync_playwright() as p:
        browser = p[browser_type].launch(headless=True)  # Use browser object from Playwright directly
        page = browser.new_page()

        page.goto(url, wait_until='load')

        page_html = BeautifulSoup(page.content(), features="html.parser")

        episodes = page_html.find_all("ul", attrs={"id": "episode_related"})

        if not episodes:
            print(f"No episode list found for URL: {url}")
            return []  # Handle case where no episode list is found

        episode_links = [
            url.split(".fi")[0] + ".fi" + i.find("a").get("href").strip() for i in episodes[0]
        ]  # Extract episode links from the first 'ul' with id 'episode_related'

        for i in episode_links[:2]:
            print(i)
            page = browser.new_page()
            page.goto(i, wait_until='load')

            page_html = BeautifulSoup(page.content(), features="html.parser")

            print(page_html.find("li", attrs={'class': "dowloads"}).find("a").get('href'))

        browser.close()

        # return episode_links

# Example usage
url = "https://ww17.gogoanimes.fi/category/boku-no-hero-academia-7th-season-dub"
episode_links = scrape_episode_links_from_first_page(url)

# if episode_links:
#     print(f"First episode link: {episode_links[0]}")
# else:
#     print("Episode link extraction failed.")

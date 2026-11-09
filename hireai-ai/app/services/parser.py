import fitz # PyMuPDF
from typing import Optional

class DocumentParser:
    def parse_pdf(self, file_path: str) -> str:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    async def scrape_url(self, url: str) -> str:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto(url, wait_until="networkidle")
                text = await page.inner_text("body")
                await browser.close()
                return text
            except Exception as e:
                await browser.close()
                return f"Error scraping {url}: {str(e)}"

parser = DocumentParser()

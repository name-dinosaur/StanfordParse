import os
import base64
import json
import time
from io import BytesIO
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class PdfGenerator:
    """
    Generates PDFs from given URLs.
    """

    print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True,
        'paperWidth': 8.5,
        'paperHeight': 11,
    }

    def __init__(self, urls: List[str]):
        self.urls = urls

    def _get_pdf_from_url(self, url):
        """
        Loads the webpage and converts it to a PDF.
        """
        self.driver.get(url)
        time.sleep(5)  # Allow time for page to load

        # Use Selenium’s built-in method for Chrome DevTools Protocol
        result = self.driver.execute_cdp_cmd("Page.printToPDF", self.print_options)
        return base64.b64decode(result['data'])

    def generate_pdfs(self):
        """
        Loops through the given URLs and saves PDFs.
        """
        webdriver_options = ChromeOptions()
        webdriver_options.add_argument('--headless')
        webdriver_options.add_argument('--disable-gpu')
        webdriver_options.add_argument('--no-sandbox')
        webdriver_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=webdriver_options
        )

        for url in self.urls:
            print(f"Processing: {url}")
            pdf_data = self._get_pdf_from_url(url)
            file_name = url.split("/")[-1] + ".pdf"

            save_directory = "data"
            os.makedirs(save_directory, exist_ok=True)  # Ensure the folder exists

            file_path = os.path.join(save_directory, file_name)

            with open(file_path, "wb") as outfile:
                outfile.write(pdf_data)

            print(f"Saved: {file_path}")


        self.driver.quit()
        print("All PDFs generated successfully!")


# MAIN EXECUTION

urls = [
    "https://www.bclaws.gov.bc.ca/civix/document/id/lc/statreg/96001_01",
    "https://www.bclaws.gov.bc.ca/civix/document/id/lc/statreg/21019",
    "https://www.bclaws.gov.bc.ca/civix/document/id/lc/statreg/02036_01"
]

pdf_generator = PdfGenerator(urls)
pdf_generator.generate_pdfs()

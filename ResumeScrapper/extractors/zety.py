from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from .extractor import Extractor

class ZetyExtractor(Extractor):
    categories_url = "https://zety.com/resume-examples"
    base_url = "https://zety.com"
    
    def __init__(self) -> None:
        super().__init__()
        options = FirefoxOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=options)

    def _get_categories_div(self, soup):
        return soup.find("div", class_="categories").find("ul", class_="categories__list").find_all("li")
    
    def _get_category_id(self, category):
        return category.get("data-category")
    
    def _get_category_title(self, category):
        return category.find("span", class_="categories__label").text
    
    def _get_subcategory_div(self, category):
        return self.soup.find("div", id=self._get_category_id(category)).find_all("li")
    
    def _get_sub_category_text(self, sub_category):
        return sub_category.text
    
    def _get_sub_category_url(self, sub_category):
        return sub_category.find("a").get('href')
    
    def _get_resume_page(self, url):
        self.browser.get(url)
        return BeautifulSoup(self.browser.page_source, "html.parser")
    
    def _extract_single_resume(self, page, subcategory_data):
        content = page.find('div', class_='blog-main').find('div', class_='b-section')
        subcategory_data['resume'] = content.get_text(separator="\n").replace(u'\xa0', ' ')


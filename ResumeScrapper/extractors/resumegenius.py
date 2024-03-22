import requests
from bs4 import BeautifulSoup
from .extractor import Extractor


class ResumeGeniusExtractor(Extractor):
    categories_url = "https://resumegenius.com/resume-samples"
    base_url = "https://resumegenius.com"

    def _get_categories_div(self, soup):
        return soup.find("section", id="categories").find("ul", class_="category-list").find_all("li")
    
    def _get_category_id(self, category):
        return category.find("a").get('href')[1:]
    
    def _get_category_title(self, category):
        return category.find("span").text
    
    def _get_subcategory_div(self, category):
        return self.soup.find("div", id=self._get_category_id(category)).find_all("li")
    
    def _get_sub_category_text(self, sub_category):
        return sub_category.find("a").text
    
    def _get_sub_category_url(self, sub_category):
        return sub_category.find("a").get('href').replace('https://resumegenius.com', '')
    
    def _extract_single_resume(self, page, subcategory_data):
        subcategory_html = page.find('article', id='text-format')
        subcategory_data['resume'] = subcategory_html.get_text()

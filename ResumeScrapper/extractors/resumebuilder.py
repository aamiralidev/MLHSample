import requests
from bs4 import BeautifulSoup
from .extractor import Extractor

class ResumeBuilderExtractor(Extractor):
    categories_url = "https://www.resumebuilder.com/resume-examples/"
    base_url = "https://www.resumebuilder.com"

    def _get_categories_div(self, soup):
        return soup.find("article", class_="article").find_all("table")
    
    def _get_category_id(self, category):
        return None
    
    def _get_category_title(self, category):
        return category.find("th").text
    
    def _get_subcategory_div(self, category):
        return category.find_all("td")
    
    def _get_sub_category_text(self, sub_category):
        return sub_category.find('a').text
    
    def _get_sub_category_url(self, sub_category):
        return sub_category.find("a").get('href')
    
    def _extract_single_resume(self, page, subcategory_data):
        subcategory_html = page.find('article')
        tab_ids = [elem.get('data-tab_id') for elem in subcategory_html.find('ul', class_='tabs').find_all('li')]
        tab_ids = zip(['entry-level', 'mid-career', 'senior-level'], tab_ids)

        for key, id in tab_ids:
            res = page.find('div', id=id)
            res = res.get_text().replace(u'\xa0', ' ')
            subcategory_data[key] = res


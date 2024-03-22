import requests
from bs4 import BeautifulSoup
import abc
from copy import deepcopy

class Extractor(abc.ABC):
    categories_url = None
    base_url = None

    def __init__(self) -> None:
        self.soup = self._get_categories_page()
        self.categories_div = self._get_categories_div(self.soup)
        self.categories_data = {}

    def _get_categories_page(self):
        response = requests.get(self.categories_url)
        return BeautifulSoup(response.content, "html.parser")
    
    def _get_resume_page(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.content, "html.parser")
    
    def extract_resume_categories(self):
        for category in self.categories_div:
            try:
                category_data = {'id': self._get_category_id(category)}
                category_title = self._get_category_title(category)
                category_div = self._get_subcategory_div(category)
                category_data["subcategories"] = self._get_sub_categories(category_div)
                self.categories_data[category_title] = category_data
            except Exception as e:
                # print(e)
                pass 
        return self.categories_data
    
    def _get_sub_categories(self, category):
        subcategories = {}
        for sub_category in category:
            try:
                subcategory_text = self._get_sub_category_text(sub_category)
                subcategories[subcategory_text] = { "url": self._get_sub_category_url(sub_category) }
            except:
                pass

        return subcategories 
    
    def extract_resumes(self, categories_data):
        data = deepcopy(categories_data)
        # x=0
        for _, category_data in data.items():
            for subcategory_text, subcategory_data in category_data["subcategories"].items():
                try:
                    subcategory_relative_url = subcategory_data["url"]
                    subcategory_full_url = f"{self.base_url}{subcategory_relative_url}"
                    soup = self._get_resume_page(subcategory_full_url)
                    self._extract_single_resume(soup, subcategory_data)
                    print(f"Fetching resume: {subcategory_text}")
                except Exception as e:
                    print(f"Error: Fetching resume: {subcategory_text}")
                    print(e)

            #     x+=1
            #     if x>2:
            #         break
            # break
        return data

    def _extract_single_resume(self, page, subcategory_data):
        pass

    @abc.abstractmethod
    def _get_categories_div(self, soup):
        pass

    @abc.abstractmethod
    def _get_subcategory_div(self, category):
        pass

    @abc.abstractmethod
    def _get_category_id(self, category):
        pass 

    @abc.abstractmethod
    def _get_category_title(self, category):
        pass 

    @abc.abstractmethod
    def _get_sub_category_text(self, sub_category):
        pass 

    @abc.abstractmethod
    def _get_sub_category_url(self, sub_category):
        pass 

    
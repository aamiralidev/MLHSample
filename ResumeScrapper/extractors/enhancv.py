from .extractor import Extractor

class EnhanCVExtractor(Extractor):
    categories_url = "https://enhancv.com/resume-examples/"

    def _get_categories_div(self, soup):
        return soup.find("div", class_="blog-article").find_all(recursive=False)
    
    def _get_category_id(self, category):
        return category.find('div').get('id')
    
    def _get_category_title(self, category):
        return category.find("h2").text
    
    def _get_subcategory_div(self, category):
        return category.find("div").find_all(recursive=False)[1].find_all("a")
    
    def _get_sub_category_text(self, sub_category):
        return sub_category.find('p').text
    
    def _get_sub_category_url(self, sub_category):
        return sub_category.get('href')

if __name__ == "__main__":
    extractor = EnhanCVExtractor()
    categories_data = extractor.extract_resume_categories()
    # extractor.extract_resumes(categories_data)
    print(categories_data)
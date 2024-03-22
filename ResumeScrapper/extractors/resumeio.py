from .extractor import Extractor

class ResumeIOExtractor(Extractor):
    categories_url = "https://resume.io/resume-examples"

    def _get_categories_div(self, soup):
        return soup.find_all("div", class_="examples-category-card")
    
    def _get_category_id(self, category):
        return category.get('id')[:-2]
    
    def _get_category_title(self, category):
        return category.find("div", class_='examples-category-card__name').text
    
    def _get_subcategory_div(self, category):
        return category.find_all("a")
    
    def _get_sub_category_text(self, sub_category):
        return sub_category.get('data-title')
    
    def _get_sub_category_url(self, sub_category):
        return sub_category.get("href").replace('https://resume.io', '')
    
    def extract_sub_categories(self, categories_data):
        return super().extract_sub_categories(categories_data)

if __name__ == "__main__":
    extractor = ResumeIOExtractor()
    categories_data = extractor.extract_resume_categories()
    print(categories_data)
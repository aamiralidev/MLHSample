from .extractor import Extractor

class ResumeExampleExtractor(Extractor):
    categories_url = "https://resume-example.com/cv/"

    def _get_categories_div(self, soup):
        categories_div = soup.find("div", id="main-content").find_all("div", class_="et_pb_text_inner")[2]
        ul = categories_div.find_all("ul", class_="su-posts-list-loop")
        h2 = categories_div.find_all("h2")
        return zip(h2, ul)
    
    def _get_category_id(self, category):
        return category[0].get('id')
    
    def _get_category_title(self, category):
        return category[0].text
    
    def _get_subcategory_div(self, category):
        return category[1].find_all("a")
    
    def _get_sub_category_text(self, sub_category):
        return sub_category.text
    
    def _get_sub_category_url(self, sub_category):
        return sub_category.get('href')

    def extract_sub_categories(self, categories_data):
        return super().extract_sub_categories(categories_data)

if __name__ == "__main__":
    extractor = ResumeExampleExtractor()
    print(extractor.extract_resume_categories())


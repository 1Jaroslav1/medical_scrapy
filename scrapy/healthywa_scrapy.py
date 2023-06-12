from .scrapy import Scrapy
import json


class HealthwaScrapy:
    def __init__(self):
        self.URL_BASE = "https://www.healthywa.wa.gov.au/"

    def get_label_list(self):
        soup = Scrapy.get_subpage_soup(self.URL_BASE, "/Health-conditions/Health-conditions-A-to-Z")

        main_div = soup.find_all("div", {"class": "az-results"})
        label_list = main_div[0].find_all("a")

        return label_list

    def run_scrapy(self, save_path):
        label_list = self.get_label_list()
        scrapy_dict = []

        for label_tag in label_list:
            print(label_tag.contents[0].strip(),)
            text = ""

            label_soup = Scrapy.get_subpage_soup(self.URL_BASE, label_tag["href"])

            label_main_div = label_soup.find_all("div", {"id": "contentText"})

            if not label_main_div:
                continue

            all_elems = label_main_div[0].find_all(["div", "p", "ul", "h2"])

            for item in all_elems:
                text += item.get_text().strip()

            scrapy_dict.append({
                "data": {
                    "title": label_tag.contents[0].strip(),
                    "text": text,
                }
            })

        with open(save_path, "w") as json_file:
            json.dump(scrapy_dict, json_file)

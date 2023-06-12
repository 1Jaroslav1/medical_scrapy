from .scrapy import Scrapy
import json
import re


class SeattlechildrenScrapy:
    def __init__(self):
        self.URL_BASE = "https://www.seattlechildrens.org/"

    def get_label_list(self):
        soup = Scrapy.get_subpage_soup(self.URL_BASE, "/conditions/a-z/")

        main_div = soup.find_all("div", {"class": "bd"})
        li_list = main_div[2].find_all("ul", {"class": "vlist no-bullets body-medium"})
        label_list = []

        for li_item in li_list:
            labels = li_item.find_all("a")
            label_list += labels

        return label_list

    def run_scrapy(self, save_path):
        label_list = self.get_label_list()
        scrapy_dict = []

        for label_tag in label_list:
            print(label_tag.contents[0].strip(),)
            text = ""

            label_soup = Scrapy.get_subpage_soup(self.URL_BASE, label_tag["href"])

            label_main_div = label_soup.find_all("div", {"id": "main-content"})

            all_elems = label_main_div[0].find_all(["p", "ul", "h2"])
            for item in all_elems:
                new_text_part = item.get_text().strip()

                res, _ = re.subn('\n+', '\n', new_text_part)

                text += res + "\n"

            scrapy_dict.append({
                "data": {
                    "title": label_tag.contents[0].strip(),
                    "text": text,
                }
            })

        with open(save_path, "w") as json_file:
            json.dump(scrapy_dict, json_file)

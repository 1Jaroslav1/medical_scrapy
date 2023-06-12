from .scrapy import Scrapy
import json

class NhisnformScrapy:
    def __init__(self):
        self.URL_BASE = "https://www.nhsinform.scot"

    def get_label_list(self):
        soup = Scrapy.get_subpage_soup(self.URL_BASE, "/illnesses-and-conditions/a-to-z")
        label_list = soup.find_all("a", {"class": "nhs-uk__az-link"})

        return label_list

    def run_scrapy(self, save_path):
        label_list = self.get_label_list()
        scrapy_dict = []

        for label_tag in label_list:
            print(label_tag)
            label_soup = Scrapy.get_subpage_soup(self.URL_BASE, label_tag["href"])

            if not label_soup:
                continue

            main_div = label_soup.find_all("div", {"class": "js-guide cf guide"})

            if not main_div:
                continue

            label_sublist = main_div[0].find_all("a", {"class": "js-guide__link guide__link"})

            text = ""

            for sub_label in label_sublist:
                sub_label_soup = Scrapy.get_subpage_soup(self.URL_BASE, label_tag["href"] + sub_label["href"])
                if not sub_label_soup:
                    continue

                current = sub_label_soup.find_all("div", {"id": sub_label["href"][1:]})

                if not current:
                    continue

                editors = current[0].find_all("div", {"class": "editor"})

                if not editors:
                    continue

                for editor in editors:
                    all_elems = editor.find_all(["p", "ul", "h2"])

                    for item in all_elems:
                        text += item.get_text() + "\n"
                text += "\n\n"

            scrapy_dict.append({
                "data": {
                    "title": label_tag.contents[0].strip(),
                    "text": text,
                }
            })

        with open(save_path, "w") as json_file:
            json.dump(scrapy_dict, json_file)
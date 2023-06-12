from .scrapy import Scrapy
import json
import re


class EveryDayHealthScrapy:
    def __init__(self):
        self.URL_BASE = "https://www.everydayhealth.com/"

    def get_label_list(self):
        soup = Scrapy.get_subpage_soup(self.URL_BASE, "conditions/")
        main_div = soup.find_all("div", {"class": "topicslist__wrapper"})

        ul_list = main_div[0].find_all("ul", {"class": "topicslist__topiccolumncont-ul"})

        label_list = []

        for ul_item in ul_list:
            labels = ul_item.find_all("a")
            label_list += labels

        return label_list

    def run_scrapy(self, save_path):
        label_list = self.get_label_list()
        scrapy_dict = []

        for label_tag in label_list:
            print(label_tag.contents[0].strip(),)
            text = ""

            label_soup = Scrapy.get_subpage_soup(self.URL_BASE, label_tag["href"])

            if not label_soup:
                continue

            label_main_divs = label_soup.find_all("div", {"class": "eh-widget eh-widget--cb"})

            for div in label_main_divs:
                title = div.find_all("div",
                                     {"class": "eh-section-title eh-section-title--default eh-section-title--nested"})

                if title:
                    text += title[0].get_text().strip() + "\n"

                section = div.find_all("div", {"class": "eh-content-block__content"})

                if not section:
                    continue
                all_elems = section[0].find_all(["div", "p", "li", "h2"])

                for item in all_elems:
                    new_text_part = item.get_text().strip()
                    res, _ = re.subn('\n+', '\n', new_text_part)
                    text += res + "\n"

                text += "\n"

            scrapy_dict.append({
                "data": {
                    "title": label_tag.contents[0].strip(),
                    "text": text,
                }
            })

        with open(save_path, "w") as json_file:
            json.dump(scrapy_dict, json_file)

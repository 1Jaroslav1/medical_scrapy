import bs4 as bs
import urllib.request
import re
import json

class MedicalScrapy:
    def __init__(self):
        self.URL_BASE = "https://www.nhsinform.scot"

    def get_subpage_soup(self, sub_href):
        try:
            source = urllib.request.urlopen(self.URL_BASE + sub_href).read()
            soup = bs.BeautifulSoup(source, 'lxml')
            return soup
        except Exception as e:
            return None


    def get_label_list(self):
        soup = self.get_subpage_soup("/illnesses-and-conditions/a-to-z")
        label_list = soup.find_all("a", {"class": "nhs-uk__az-link"})

        return label_list

    def get_questions(self, label):
        about = f"What is {label}?"
        symptoms = f"What is symptoms of {label}"
        causes = f"What is causes of {label}?"
        treatment = f"What are the methods of treatment the {label}?"

        return [
            about,
            symptoms,
            causes,
            treatment
        ]


    def run_scrapy(self):
        label_list = self.get_label_list()
        scrapy_dict = []

        for label_tag in label_list:
            print(label_tag)
            label_name = label_tag.contents[0].strip()
            label_soup = self.get_subpage_soup(label_tag["href"])

            if not label_soup:
                continue

            main_div = label_soup.find_all("div", {"class": "js-guide cf guide"})

            if not main_div:
                continue

            label_sublist = main_div[0].find_all("a", {"class": "js-guide__link guide__link"})

            label_dict = dict()

            text = ""

            for sub_label in label_sublist:
                sub_label_soup = self.get_subpage_soup(label_tag["href"] + sub_label["href"])
                if not sub_label_soup:
                    continue

                sub_label_name = sub_label.contents[0].strip()
                # print(sub_label_name)
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
                        # print(item.get_text())
                        # if item.name == "p":
                        #     if len(item.find_all("a")) > 0:
                        #         # print(item.contents[0])
                        #         continue
                        #     else:
                        #         text += str(item.contents[0])
                        # elif item.name == "ul":
                        #     li = item.find_all("li")
                        #
                        #     for li_item in li:
                        #         if len(li_item.find_all("a")) > 0:
                        #             a_list = li_item.find_all("a")
                        #             for a_item in a_list:
                        #                 text += a_item.contents[0] + ","
                        #         else:
                        #             text += li_item.contents[0] + ","
                        # elif item.name == "h2":
                        #     text += str(item.contents[0])
                        # else:
                        #     break

                    # print(text)
                text += "\n\n"

            questions = self.get_questions(label_name)

            # for question in questions:
            #     scrapy_dict.append({
            #         "data": {
            #             "text": text,
            #             # "question": question
            #         }
            #     })

            scrapy_dict.append({
                "data": {
                    "title": label_tag.contents[0].strip(),
                    "text": text,
                }
            })

        file_path = "data3.json"
        with open(file_path, "w") as json_file:
            json.dump(scrapy_dict, json_file)

ms = MedicalScrapy()
ms.run_scrapy()


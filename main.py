from scrapy.nhsinform_scrapy import NhisnformScrapy
from scrapy.healthywa_scrapy import HealthwaScrapy
from scrapy.seattlechildren_scrapy import SeattlechildrenScrapy
from scrapy.everydayhealth_scrapy import EveryDayHealthScrapy

# scrapy = NhisnformScrapy()
# scrapy.run_scrapy("data/nhsinform/data4.json")

# scrapy = HealthwaScrapy()
# scrapy.run_scrapy("data1.json")

# scrapy = SeattlechildrenScrapy()
# scrapy.run_scrapy("data1.json")

scrapy = EveryDayHealthScrapy()
scrapy.run_scrapy("data1.json")

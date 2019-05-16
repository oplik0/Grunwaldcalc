import requests
import wptools
from time import sleep
import locale
import re
import json
class WikiScrape():
    def __init__ (self):
        while not self.checkConnection:
            sleep(1)
        self.language = locale.getdefaultlocale()[0]
        try:
            with open("./languages/"+self.language+".lang") as language_file:
                self.language_file = json.load(language_file)
        except FileNotFoundError:
            self.language = "en_US"
            with open("./languages/"+self.language+".lang") as language_file:
                self.language_file = json.load(language_file)
    def changeLanguage(self, language_code="en_US"):
        self.language = language_code
        try:
            with open("./languages/"+self.language+".lang") as language_file:
                self.language_file = json.load(language_file)
        except FileNotFoundError:
            self.language = "en_US"
            with open("./languages/"+self.language+".lang") as language_file:
                self.language_file = json.load(language_file)
            raise FileNotFoundError("Unsupported language")
    def checkConnection(self):
        if requests.get("https://en.wikipedia.org").status_code != 200:
            return False
        return True
    def getPageData(self, query):
        page = wptools.page(query, lang=self.language[:2], skip=['imageinfo', 'labels', 'query', 'querymore', 'random', 'restbase'], silent=True)
        try:
            page.get_wikidata()
            self.date_raw = page.data['claims']
        except LookupError:
            raise LookupError("Incorrect title - page doesn't exist")
        return self.date_raw

    def parseDate(self, date_raw):
        self.dates = {}
        
        # for date_format in self.language_file['date-formats']:
        #     if date_format in date_raw and not re.match(r'\+\d*\-00\-00', date_raw[date_format]):
        #         self.dates['date'] = date_raw[date_format][:date_raw[date_format].find('T')]
        #         break
        # else:
        #     for from_format, to_format in zip(self.language_file['from-formats'], self.language_file['to-formats']):
        #         if from_format in date_raw and not re.match(r'\+\d*\-00\-00', date_raw[from_format]):
        #             self.dates['from'] = date_raw[from_format][:date_raw[from_format].find('T')]
        #         if to_format in date_raw and not re.match(r'\+\d*\-00\-00', date_raw[to_format]):
        #             self.dates['to'] = date_raw[to_format][:date_raw[to_format].find('T')]
        # old, possibly easier to expand code...

        if 'P585' in date_raw:
            if len(date_raw['P585'])==2:
                self.dates["from"] = date_raw["P585"][0][:date_raw["P585"][0].find('T')]
                self.dates["to"] = date_raw["P585"][1][:date_raw["P585"][1].find('T')]
            else:
                self.dates["date"] = date_raw["P585"]
        elif 'P580' in date_raw and 'P582' in date_raw:
            self.dates["from"] = date_raw["P580"][:date_raw["P580"].find('T')]
            self.dates["to"] = date_raw["P582"][:date_raw["P580"].find('T')]
        else:
            raise LookupError("Date not found")
        return self.dates
    def findEventDate(self, event):
        date_raw = self.getPageData(event)
        return self.parseDate(date_raw)
if __name__=="__main__":
    scraper = WikiScrape()
    print('The date is: '+str(scraper.findEventDate(input("input event: "))))
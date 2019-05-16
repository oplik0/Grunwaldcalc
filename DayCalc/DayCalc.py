import locale
import json
class Calculate():
    def __init__(self):
        self.date_format = 'YYYYMMDD'
        self.date = {}
        self.language = locale.getdefaultlocale()[0]
        try:
            with open("./languages/"+self.language+".lang", encoding="UTF-8", encoding="UTF-8") as language_file:
                self.language_file = json.load(language_file)
        except FileNotFoundError:
            self.language = "en_US"
            with open("./languages/"+self.language+".lang", encoding="UTF-8", encoding="UTF-8") as language_file:
                self.language_file = json.load(language_file)
    def changeLanguage(self, language_code="en_US"):
        self.language = language_code
        try:
            with open("./languages/"+self.language+".lang", encoding="UTF-8", encoding="UTF-8") as language_file:
                self.language_file = json.load(language_file)
        except FileNotFoundError:
            self.language = "en_US"
            with open("./languages/"+self.language+".lang", encoding="UTF-8", encoding="UTF-8") as language_file:
                self.language_file = json.load(language_file)
            raise FileNotFoundError("Unsupported language")
    def changeDateFormat(self, date_format="DDMMYYYY"):
        correct_format = ''.join(char for char in date_format if char.isalpha())
        if len(correct_format) in ["DDMMYYYY", "DDYYYYMM", "MMDDYYYY", "MMYYYYDD", "YYYYMMDD", "YYYYDDMM"]:
            self.date_format = correct_format
        else:
            raise ValueError('date_format should be a string consisting of 2 "D" (Day), 2 "M" (Month) and 4 "Y" (Year) character groups in any order')
    def convertStringToDict(self, input_date="11111111"):
        correct_input_date = ''.join(char for char in input_date if char.isnumeric())
        self.date = {"year":"", "month":"", "day":""}
        if len(correct_input_date)!=len(self.date_format):
            raise ValueError("Incorrect date")
        for num, part in zip(correct_input_date, self.date_format):
            if part=="D":
                self.date["day"]+=num
            elif part=="M":
                self.date["month"]+=num
            elif part=="Y":
                self.date["year"]+=num
        return self.date
    def calculateWeekday(self, date={"year":"0000", "month":"00", "day":"00"}):
        if date=={"year":"0000", "month":"00", "day":"00"} and self.date!={}: date=self.date
        date["month"] = date["month"].replace('01', '13').replace('02', '14')
        day = int(date["day"])
        month = int(date["month"])
        year = int(date["year"][2:])
        century = int(date["year"][:2])
        if int(date["year"])>1582 or (date["year"]=='1582' and 10<=int(date["month"])<13 and int(date["day"])>15):
            weekday_raw = (day+int(13*(month+1)/5)+year+int(year/4)+int(century/4)-2*century)%7
        else:
            weekday_raw = (day+int(13*(month+1)/5)+year+int(year/4)+5-century)%7
        self.weekday = (weekday_raw+5)%7+1
        return self.weekday
    def convertWeekdayToString(self, weekday=-1):
        if weekday==-1 and self.weekday>=0:
            weekday=self.weekday
        weekdays = self.language_file["weekdays"]
        return weekdays[weekday-1]

    def findWeekday(self, input_date):
        date = self.convertStringToDict(input_date=input_date)
        weekday_raw = self.calculateWeekday(date=date)
        weekday = self.convertWeekdayToString(weekday_raw)
        return weekday

if __name__=="__main__":
    calc = Calculate()

    print(calc.findWeekday(input("Input date: ")))
    input("---Press enter to finish---")

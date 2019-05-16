from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import ConfigParser
from kivy.uix.settings import Settings
from kivy.core.window import Window
from kivy.config import Config
from DateFinder import DateFinder
from DayCalc import DayCalc

import locale
import json
Window.size = (350, 250)
class mainApp(App):
    def build(self):
        Window.clearcolor=(228./255., 228./255., 228./255., 1)
        self.title = "GrunwaldCalc"
        
        
        Window.minimum_width=300
        Window.minimum_height=200
        

        self.config = ConfigParser()
        self.config.read("config.ini")
        self.config.adddefaultsection("Settings")
        
        self.config.setdefault("Settings", "Language", locale.getdefaultlocale()[0])
        self.language = self.config.getdefault("Settings", "Language", locale.getdefaultlocale()[0])
        self.settings = Settings()
        self.day_calc = DayCalc.Calculate()
        self.date_finder = DateFinder.WikiScrape()
        self.day_calc.changeLanguage(self.language)
        self.date_finder.changeLanguage(self.language)
        self.container = BoxLayout(orientation="vertical")
        self.search_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.25), height=100)
        self.results_layout = AnchorLayout(anchor_y="top")
        self.container.add_widget(self.search_layout)
        self.container.add_widget(self.results_layout)

        try:
            with open("./languages/"+self.language+".lang", encoding="UTF-8") as language_file:
                self.language_file = json.load(language_file)
        except FileNotFoundError:
            self.language = "en_US"
            with open("./languages/"+self.language+".lang", encoding="UTF-8") as language_file:
                self.language_file = json.load(language_file)

        self.search_box = TextInput(hint_text=(self.language_file["hint"]), size_hint=(0.7, None), height=50, multiline=False)
        self.search_button = Button(text=self.language_file["button-text"], size_hint=(0.3, None), height=50)
        self.search_layout.add_widget(self.search_box)
        self.search_layout.add_widget(self.search_button)
        

        self.search_box.bind(on_text_validate=self.start_main)
        self.search_button.bind(on_press=self.start_main)

        return self.container

    def start_main(self, instance):
        text_value = ''.join(char for char in self.search_box.text if char.isnumeric())
        if 4<len(text_value)<9:
            self.results_layout.clear_widgets()
            self.date = self.day_calc.findWeekday(text_value)
            self.result_label = Label(text=self.language_file["single-date"].format(self.date), markup=True)
            self.results_layout.add_widget(self.result_label)
        else:
            self.results_layout.clear_widgets()
            try:
                self.event_dates=(self.date_finder.findEventDate(self.search_box.text))
            
                self.event_weekdays = []
                for date in self.event_dates:
                    self.event_weekdays.append(self.day_calc.findWeekday(self.event_dates[date]))
                if len(self.event_dates) == 2:
                    self.result_label = Label(text=self.language_file["from-to-date"].format(self.event_dates['from'], self.event_weekdays[0], self.event_dates['to'], self.event_weekdays[1]), markup=True, size_hint=(1, None))
                    self.result_label.text_size=(self.results_layout.width-40, self.results_layout.height)

                    self.results_layout.add_widget(self.result_label)
                else:
                    self.result_label = Label(text=self.language_file["from-to-date"].format(self.event_dates['date'], self.event_weekdays[0]), markup=True, size_hint=(1, None))
                    self.result_label.text_size=(self.results_layout.width-40, self.results_layout.height)

                    self.results_layout.add_widget(self.result_label)
            except LookupError:
                self.result_label = Label(text=self.language_file["lookup-error"], markup=True)
                self.results_layout.add_widget(self.result_label)



if __name__ == "__main__":
    GrunwaldCalc = mainApp()
    GrunwaldCalc.run()

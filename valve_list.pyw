from ttkthemes import themed_tk as tk
from tkinter import ttk
import csv

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        root.wm_title("Valve Register")
        root.iconbitmap(default='./icon.ico')
        root.set_theme("arc")
        self.pack()
        self.create_widgets()

    #create some widgets
    def create_widgets(self):

        self.search_label = ttk.Label(self)
        self.search_label["text"] = "Search"
        self.search_label.pack(side="top")
        
        self.search_entry = ttk.Entry(self)
        self.search_entry.bind("<Return>", self.search)
        self.search_entry["width"] = 30
        self.search_entry.pack(side="top")

        self.selection = ttk.Combobox(self)
        self.selection['values'] = self.get_valve_names()
        self.selection.set("Please Select")
        self.selection["width"] = 27
        self.selection.bind("<<ComboboxSelected>>", self.display_data)  
        self.selection.pack(side="top")

        self.data = ttk.Label(self)
        self.data["width"] = 80
        self.data.pack(side="top")

        self.quit = ttk.Button(self)
        self.quit["text"] = "QUIT"
        self.quit["command"] = root.destroy
        self.quit.pack(side="top")

        self.copyright_label = ttk.Label(self)
        self.copyright_label["text"] = "© Joseph Douce 2018"
        self.copyright_label.pack(side="top")

    #load valve data into a lsit of dictionaries
    def load_data(self):
        with open('./valve_list.csv') as f:
            data = [{k: str(v) for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]
        return(data)

    #get list of valve names from valve data
    def get_valve_names(self):
        valves = []
        for item in self.load_data():
            valves.append(item['VALVE'])
        return(valves)

    #get data from selected valve and convert it into a user readable format
    def display_data(self, *args):
        for item in self.load_data():
            if item['VALVE'] == self.selection.get():
                dsiplay_text = ""
                for key in item.keys():
                    dsiplay_text = dsiplay_text + key + ' : ' + item[key] + "\n \n"
                self.data["text"] = dsiplay_text.upper()

    #search list of valves for valves containing search term
    def search(self, event):
        search_term = self.search_entry.get()
        results = []
        for item in self.get_valve_names():
            if search_term in item:
                results.append(item)
        self.selection['values'] = results
        if len(results) == 0:
            self.selection.set("No Results Found")
            self.data["text"] = ""
        elif len(results) == 1:
            self.selection.set(results[0])
            self.display_data()
        else:
            self.selection.set("Please Select")
            self.data["text"] = ""

#launch app      
if __name__ == '__main__':
    root = tk.ThemedTk()
    app = Application(master=root)
    app.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class MainPageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Selection Robot")
        self.root.geometry("1400x700+50+50")
        self.hotels = []
        self.attributes = {
            "Cleanliness": 0.115889,
            "Room": ((0.114399+0.24)/2),
            "Service": 0.116970,
            "Location": 0.110330,
            "Value": 0.111267,
            "Safety": 0.104538,
            "Comfort": ((0.108339+0.34)/2),
            "Transportation": 0.110073,
            "Noise": 0.108196
        }
        self.attribute_indices = {
            "Cleanliness": 3,
            "Room": 4,
            "Service": 5,
            "Location": 6,
            "Value": 7,
            "Safety": 8,
            "Comfort": 9,
            "Transportation": 10,
            "Noise": 11
        }

        # Initialize the Database object
        self.db = Database("hotels.db")

        self.setup_ui()

    def setup_ui(self):
        self.city_combo = ttk.Combobox(self.root, values=["Beijing", "Dubai", "Chicago", "Las Vegas",
                                                          "London", "Montreal", "New Delhi",
                                                          "San Francisco", "Shanghai", "New York City"], state='readonly', width=20)
        self.city_combo.set("Beijing")
        self.city_combo.place(x=30, y=10)

        search_button = ttk.Button(self.root, text="Search", width=30, command=self.search_hotels)
        search_button.place(x=200, y=9)

        pick_label = tk.Label(self.root, text="Pick max. three attributes", font=('Helvetica', 9))
        pick_label.place(x=30, y=42)

        self.vars = []
        checkbox_y = 70

        for attribute in self.attributes:
            var = tk.IntVar()
            checkbox = ttk.Checkbutton(self.root, text=attribute, variable=var,
                                       command=lambda v=var: self.check_limit(v), width=15)
            checkbox.place(x=30, y=checkbox_y)
            checkbox_y += 25
            self.vars.append(var)

        self.tree = ttk.Treeview(self.root, columns=[], show='headings', height=20)
        self.tree.place(x=200, y=42, width=1170, height=600)

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.place(x=1370, y=42, height=600)
        self.tree.configure(yscroll=scrollbar.set)

    def check_limit(self, current_var):
        count = sum(v.get() for v in self.vars)
        if count > 3:
            current_var.set(0)

    def search_hotels(self):
        city = self.city_combo.get()
        selected_attributes = [attr for attr, var in zip(self.attributes, self.vars) if var.get()]

        if len(selected_attributes) == 0:
            messagebox.showerror("Selection Error", "Please select at least one attribute.")
            return
        elif len(selected_attributes) > 3:
            messagebox.showerror("Selection Error", "Please select up to 3 attributes.")
            return

        self.hotels = self.db.select_hotels_by_city(city)

        if self.hotels is None:
            self.hotels = []

        if not self.hotels:
            messagebox.showinfo("No Results", "No hotels found for the selected city.")
            return

        self.hotels = self.calculate_scores(self.hotels, selected_attributes)

        self.hotels.sort(key=lambda x: x[-1], reverse=True)
        self.display_results()

    def calculate_scores(self, hotels, selected_attributes):
        coefficients = self.attributes
        scored_hotels = []
        for hotel in hotels:
            score = sum(float(hotel[self.attribute_indices[attr]]) * coefficients[attr] for attr in selected_attributes)
            scored_hotels.append(list(hotel) + [score])  # Convert tuple to list before appending the score
        return scored_hotels

    def display_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Define all columns to be displayed
        columns = ['Hotel Name'] + list(self.attributes.keys())
        self.tree.config(columns=columns)

        self.tree.heading('Hotel Name', text='Hotel Name', anchor='w')
        self.tree.column('Hotel Name', anchor='w', width=200)  # Wider width for hotel name

        for col in self.attributes.keys():
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, anchor='w', width=20)

        for hotel in self.hotels:
            values = [hotel[2]]
            for attr in self.attributes.keys():
                index = self.attribute_indices[attr]
                values.append(f"{float(hotel[index]):.2f}")
            self.tree.insert('', 'end', values=values)


root = tk.Tk()
app = MainPageGUI(root)
root.mainloop()

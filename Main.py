import tkinter
import csv
from tkinter import Toplevel, ttk, Label, Text, Scrollbar, Entry, messagebox, Spinbox, Listbox
from tkinter import *
from datetime import datetime
import os

# All the different classes i needed
class Restaurant:
    def __init__(self, restaurant_id, name, cuisine_type, rating, location, total_tables, table_configuration, opening_hours, closing_hours):
        self.restaurant_id = restaurant_id
        self.name = name
        self.cuisine_type = cuisine_type
        self.rating = rating
        self.location = location
        self.total_tables = total_tables
        self.table_configuration = table_configuration
        self.opening_hours = opening_hours
        self.closing_hours = closing_hours

    def get_available_tables(self, date, time, party_size):
        available_tables = []
        with open("bookings.csv", 'r') as bookings_file:
            reader = csv.DictReader(bookings_file)
            booked_tables = [row['table_id'] for row in reader if row['restaurant_id'] == self.restaurant_id and row['date'] == date and row['time'] == time]
        for table in self.table_configuration:
            if table['size'] >= party_size and table['id'] not in booked_tables:
                available_tables.append(table)
        return available_tables

    def check_valid_booking_time(self, time):
        return self.opening_hours <= time <= self.closing_hours

    def display_restaurant_info(self):
        return f"{self.name} ({self.cuisine_type})\nRating: {self.rating}/5\nLocation: {self.location}\nOperating Hours: {self.opening_hours} - {self.closing_hours}"

    def to_csv(self):
        return [self.restaurant_id, self.name, self.cuisine_type, self.rating, self.location, self.total_tables, self.table_configuration, self.opening_hours, self.closing_hours]

class User:
    def __init__(self, user_id, name, email, phone_number):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.current_bookings = []

class Booking:
    def __init__(self, booking_id, restaurant_id, user_id, date, time, table_id, party_size):
        self.booking_id = booking_id
        self.restaurant_id = restaurant_id
        self.user_id = user_id
        self.date = date
        self.time = time
        self.table_id = table_id
        self.party_size = party_size

#Dealing with all the different files
def initialize_files():
    if not os.path.exists("restaurants.csv"):
        with open("restaurants.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["restaurant_id", "name", "cuisine_type", "rating", "location", "total_tables", "table_configuration", "opening_hours", "closing_hours"])

    if not os.path.exists("users.csv"):
        with open("users.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "name", "email", "phone_number"])

    if not os.path.exists("bookings.csv"):
        with open("bookings.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["booking_id", "user_id", "restaurant_id", "date", "time", "table_id", "party_size"])


# File handlers
def get_restaurants():
    try:
        with open("restaurants.csv", 'r') as file_restaurants:
            restaurant_contents = list(csv.DictReader(file_restaurants))
            return restaurant_contents
    except OSError as e:
        messagebox.showerror("Error", "The file restaurants.csv does not exist.")
        return []

def user_data():
    try:
        with open("users.csv", 'r') as user_data:
            user_contents = list(csv.DictReader(user_data))
            return user_contents
    except OSError as e:
        messagebox.showerror("Error", "The file users.csv does not exist.")
        return []

def booking_data():
    try:
        with open("bookings.csv", 'r') as booking_data_as_file:
            booking_contents = list(csv.DictReader(booking_data_as_file))
            return booking_contents
    except OSError as e:
        messagebox.showerror("Error", "The file bookings.csv does not exist.")
        return []

# GUI Main Page
win = tkinter.Tk(className="Restaurants")
win.title("Restaurant Booking System")
win.resizable(width=True, height=True)

title = tkinter.Label(win, text="Restaurant Booking System")
title.pack()

#Restaurant list part
def restaurant_list():
    file_contents = get_restaurants()
    new_window = Toplevel(win)
    new_window.title("Restaurant List")
    new_window.geometry("400x300")
    new_window.resizable(width=True, height=True)

    title_1 = tkinter.Label(new_window, text="Restaurant List", font=("Times New Roman", 16))
    title_1.pack(pady=10)

    frame = tkinter.Frame(new_window)
    frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    scrollbar = tkinter.Scrollbar(frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    restaurant_list_to_show = tkinter.Listbox(frame, yscrollcommand=scrollbar.set)
    for restaurant in file_contents:
        restaurant_list_to_show.insert(END, f"{restaurant['name']} - {restaurant['cuisine_type']} - {restaurant['rating']}/5")

    restaurant_list_to_show.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=restaurant_list_to_show.yview)

    # Function to add new restaurants
    def adding_restaurants():
        restaurant_addition_window = Toplevel(new_window)
        restaurant_addition_window.title("Add Restaurant")
        restaurant_addition_window.geometry("400x400")

        labels = ["Restaurant ID", "Name", "Cuisine Type", "Rating", "Location", "Total Tables", "Table Configuration", "Opening Hours", "Closing Hours"]
        entries = []
        for i, label_text in enumerate(labels):
            Label(restaurant_addition_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(restaurant_addition_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def save_restaurant():
            with open("restaurants.csv", 'a', newline='') as restaurants_file:
                writer = csv.writer(restaurants_file)
                writer.writerow([entry.get() for entry in entries])
            messagebox.showinfo("Success", "Restaurant added successfully!")
            restaurant_addition_window.destroy()

        Button(restaurant_addition_window, text="Add Restaurant", command=save_restaurant).grid(row=len(labels), columnspan=2, pady=10)

    add_button = tkinter.Button(new_window, text="Add a Restaurant", command=adding_restaurants)
    add_button.pack(pady=5)

#Table booking thing
def bookings():
    # Setting the window up
    bookings_window = Toplevel(win)
    bookings_window.title("Make a Reservation")
    bookings_window.geometry("400x300")
    bookings_window.resizable(width=True, height=True)

    # Choosing the date
    Label(bookings_window, text="Select Date (DD-MM-YYYY)").pack(pady=5)
    date_input = Entry(bookings_window)
    date_input.pack(pady=5)

    # Party Size
    Label(bookings_window, text="Select Party Size").pack(pady=5)
    party_size_input = Spinbox(bookings_window, from_=1, to=20)
    party_size_input.pack(pady=5)

    # Time
    Label(bookings_window, text="Select Time (HH:MM)").pack(pady=5)
    time_input = Entry(bookings_window)
    time_input.pack(pady=5)

    # Restaurant ID
    Label(bookings_window, text="Enter Restaurant ID").pack(pady=5)
    restaurant_id_input = Entry(bookings_window)
    restaurant_id_input.pack(pady=5)

    # Adding the booking to user profile
    Label(bookings_window, text="Enter USER ID").pack(pady=5)
    user_id_input = Entry(bookings_window)
    user_id_input.pack(pady=5)

    def confirm_booking():
        booking_id = f"B-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        with open("bookings.csv", 'a', newline='') as bookings_file:
            writer = csv.writer(bookings_file)
            writer.writerow([
                booking_id,
                user_id_input.get(),
                restaurant_id_input.get(),
                date_input.get(),
                time_input.get(),
                "TABLE_ID",
                party_size_input.get()
            ])
        messagebox.showinfo("Success", f"Booking confirmed! Your booking ID is {booking_id}.")
        bookings_window.destroy()

    # Add the confirm button - this should be inside bookings() but outside confirm_booking()
    Button(bookings_window, text="Confirm Booking", command=confirm_booking).pack(pady=10)
# Login page
def login_page():
    login_window = Toplevel(win)
    login_window.title("Login")
    login_window.geometry("400x300")

    Label(login_window, text="User ID").grid(row=0, column=0, padx=10, pady=5)
    Label(login_window, text="Email").grid(row=1, column=0, padx=10, pady=5)

    user_id_input = Entry(login_window)
    email_input = Entry(login_window)
    user_id_input.grid(row=0, column=1, padx=10, pady=5)
    email_input.grid(row=1, column=1, padx=10, pady=5)
#Checking the user
    def authenticate_user():
        users = user_data()
        for user in users:
            if user['user_id'] == user_id_input.get() and user['email'] == email_input.get():
                messagebox.showinfo("Success", "Login successful!")

                # Create bookings window after successful login
                bookings_window = Toplevel(login_window)
                bookings_window.title(f"Bookings for User {user_id_input.get()}")
                bookings_window.geometry("600x400")

                # Create main frame with scrollbar
                main_frame = Frame(bookings_window)
                main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

                # Add header
                header = Label(main_frame, text="Your Bookings", font=("Times New Roman", 16))
                header.pack(pady=10)

                # Create frame for the listbox and scrollbar
                list_frame = Frame(main_frame)
                list_frame.pack(fill=BOTH, expand=True)

                # Add scrollbar
                scrollbar = Scrollbar(list_frame)
                scrollbar.pack(side=RIGHT, fill=Y)

                # Create listbox
                bookings_list = Listbox(list_frame, yscrollcommand=scrollbar.set, width=70)
                bookings_list.pack(side=LEFT, fill=BOTH, expand=True)
                scrollbar.config(command=bookings_list.yview)

                # Get and display all bookings for this user
                all_bookings = booking_data()
                restaurants = get_restaurants()
                restaurant_dict = {r['restaurant_id']: r for r in restaurants}

                # Populate the listbox with bookings
                for booking in all_bookings:
                    if booking['user_id'] == user_id_input.get():
                        restaurant = restaurant_dict.get(booking['restaurant_id'], {'name': 'Unknown Restaurant'})
                        booking_info = (
                            f"Booking ID: {booking['booking_id']} | "
                            f"Restaurant: {restaurant['name']} | "
                            f"Date: {booking['date']} | "
                            f"Time: {booking['time']} | "
                            f"Party Size: {booking['party_size']}"
                        )
                        bookings_list.insert(END, booking_info)

                if bookings_list.size() == 0:
                    bookings_list.insert(END, "No bookings found")

                return
        #Else if the user is not there, ask them to create an account
        result = messagebox.askquestion("Error", "Would you like to create an account? ")
        if result == 'yes':
            create_account()

    def create_account():
        account_window = Toplevel(login_window)

        Label(account_window, text="User ID").grid(row=0, column=0, padx=10, pady=5)
        Label(account_window, text="Name").grid(row=1, column=0, padx=10, pady=5)
        Label(account_window, text="Email").grid(row=2, column=0, padx=10, pady=5)
        Label(account_window, text="Phone Number").grid(row=3, column=0, padx=10, pady=5)

        user_id_input = Entry(account_window)
        name_input = Entry(account_window)
        email_input = Entry(account_window)
        phone_input = Entry(account_window)

        user_id_input.grid(row=0, column=1, padx=10, pady=5)
        name_input.grid(row=1, column=1, padx=10, pady=5)
        email_input.grid(row=2, column=1, padx=10, pady=5)
        phone_input.grid(row=3, column=1, padx=10, pady=5)

        def save_user():
            with open("users.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_id_input.get(), name_input.get(), email_input.get(), phone_input.get()])
            messagebox.showinfo("Success", "Account created!")
            account_window.destroy()

        Button(account_window, text="Create Account", command=save_user).grid(row=4, column=1, pady=10)





    Button(login_window, text="Login", command=authenticate_user).grid(row=2, columnspan=2, pady=10)

# Buttons on Main Page
Button(win, text="View Restaurants", command=restaurant_list).pack(pady=5)
Button(win, text="Make a Reservation", command=bookings).pack(pady=5)
Button(win, text="Login", command=login_page).pack(pady=5)

# Initialize required files
initialize_files()

win.mainloop()


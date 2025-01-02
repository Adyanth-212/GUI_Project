**# Restaurant Booking System
## Overview
The **Restaurant Booking System** is a Python-based desktop application designed to facilitate the management of restaurant reservations. It provides a convenient way for users to browse restaurants, make reservations, and manage their bookings. The system features an intuitive GUI built with the `tkinter` library and handles the data using CSV files for simplicity.
## Features
1. **Restaurant Management**:
    - View a list of available restaurants along with their details (name, cuisine type, location, and rating).
    - Add new restaurants to the system with details like configuration, opening/closing hours, and total tables.

2. **Reservation Management**:
    - Make table reservations for specific restaurants with user-defined date, time, and party size.
    - Ensure table availability and validate booking times based on restaurant operating hours.

3. **User Management**:
    - User login and authentication using a unique ID and email.
    - Create a user account with personal details such as name, email, and phone number.
    - View the list of all bookings made by the logged-in user.

4. **File Management**:
    - Automatic initialization of required CSV files (`restaurants.csv`, `users.csv`, and `bookings.csv`) if they don't already exist.
    - Store data in structured CSV files for restaurants, users, and bookings, simplifying data storage and retrieval.

5. **Graphical User Interface**:
    - A user-friendly GUI built with `tkinter` that offers easy navigation and handles all functionalities such as viewing lists, adding entries, and making bookings.

## How to Use
### Main Menu
- On starting the application, the main menu provides three primary options:
    - **View Restaurants**: Opens a list of all available restaurants and provides an option to add a new restaurant.
    - **Make a Reservation**: Allows users to book a table specifying the date, time, party size, and restaurant.
    - **Login**: Provides user authentication with an option to view bookings or create a new account.

### Functionalities in Detail
#### 1. **View Restaurants**:
- Displays a list of restaurants with their name, cuisine type, and rating.
- Provides a button to add a new restaurant by filling out fields such as name, location, cuisine, rating, opening/closing hours, and table configuration.

#### 2. **Make a Reservation**:
- Allows you to:
    - Select the date and time for the reservation.
    - Specify the party size and choose the restaurant by its ID.
    - Add the user ID to associate the booking with a specific user.

- Ensures that the selected time falls within the restaurant’s operating hours and checks table availability.

#### 3. **Login & User Management**:
- Authorizes the user by matching their ID and email in the `users.csv` file.
- If the user does not exist, offers an option to create a new account.
- After successful login, displays the user’s existing bookings and provides detailed information about each reservation, such as:
    - Restaurant name.
    - Date, time, and party size of the booking.

## Data Storage
The system uses plain CSV files to store its data, making it lightweight and simple to use. Below is a description of each file:
1. **restaurants.csv**:
    - Stores restaurant details, including ID, name, cuisine type, rating, location, total tables, and table configuration.

2. **users.csv**:
    - Stores user details, including unique user ID, name, email, and phone number.

3. **bookings.csv**:
    - Stores booking details, including booking ID, user ID, restaurant ID, date, time, table ID, and party size.

## Prerequisites
1. **Python 3.6 or higher**.
2. The following libraries are required:
    - `tkinter`: For GUI development.
    - `csv`: For reading and writing to CSV files.
    - `datetime`: For timestamps and validation of reservation dates and times.

## Installation & Setup
1. Clone or download the project files to your local system.
2. Install Python if not already installed on your system.
3. Run the script `restaurant_booking_system.py` to start the application.
4. The system automatically initializes the required CSV files if they are not present.

## How It Works
1. **Restaurant Management**:
    - Restaurants are fetched from `restaurants.csv` and displayed in the "View Restaurants" window.
    - New restaurants can be added in the same window by filling out the relevant details and saving them to the file.

2. **Making Reservations**:
    - Before confirming a reservation:
        - The system checks the availability of tables and validates the booking time against the restaurant's operational hours.

    - Successfully reserved tables are stored in the `bookings.csv` file.

3. **User Management**:
    - During login:
        - The user details are validated from the `users.csv` file.
        - Existing reservations by the user are displayed from the `bookings.csv` file.

## Future Improvements
1. Replace CSV files with a database(SQL) for enhanced scalability and performance.
2. Add reporting/analytics features like most booked restaurants and peak reservation times.
3. Enable email notifications for booking confirmations.
4. Enhance error handling and ensure all inputs are validated to improve system reliability.(For example forcing users to enter proper gmails)
5. Add some money related things and maybe a search bar in the restuarants page
6. Add a filtering system to help search for specific cuisines and other things(like budget, hours, etc)
7. Imporve the UI of the system

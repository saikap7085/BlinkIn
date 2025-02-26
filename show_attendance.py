import os
import csv
import tkinter as tk
from tkinter import messagebox
import pyttsx3

def read_csv_files(subject):
    data = []
    directory = f'Attendance\\{subject}'
    if not os.path.exists(directory):
        messagebox.showerror("Error", "Directory does not exist.")
        engine.say("Directory does not exist.")
        engine.runAndWait()
        return data
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                first_row = True  # Flag to skip the first row
                for row in reader:
                    if first_row:
                        first_row = False
                        continue  # Skip the first row
                    # Ensure each row has exactly 3 columns
                    if len(row) == 3:
                        data.append(row)
                    else:
                        print("Ignored as it does not contain required values:", row)
    return data

def process_data(data):
    processed_data = []
    seen = set()  # To keep track of unique entries
    for entry in data:
        entry_tuple = tuple(entry)
        if entry_tuple not in seen:
            count = data.count(entry)
            cleaned_entry = [entry[0], entry[1].replace("'", '').replace('[', '').replace(']', ''), count]
            processed_data.append(cleaned_entry)
            seen.add(entry_tuple)
    return processed_data

# Function to create and display table-like structure with the processed data
def display_data_in_table(data):
    # Create a new window for displaying the table
    table_window = tk.Toplevel(root)
    table_window.title("Attendance Table")
    table_window.geometry("700x400")
    table_window.configure(bg="red")  # Set background color

    # Create headers for the table
    headers = ["Sno.", "Enrollment No.", "Name", "No. of Attendance"]
    for col, header in enumerate(headers):
        label = tk.Label(table_window, text=header, font=("Helvetica", 12, "bold"), bg="red", fg="white", relief="solid", width=15)
        label.grid(row=0, column=col, padx=5, pady=5)

    # Populate the table with processed data
    for row, entry in enumerate(data, start=1):
        # Automatically increment serial number (Sno.)
        sno_label = tk.Label(table_window, text=row, font=("Helvetica", 10), bg="red", fg="white", relief="solid", width=15)
        sno_label.grid(row=row, column=0, padx=5, pady=5)

        for col, value in enumerate(entry, start=1):
            label = tk.Label(table_window, text=value, font=("Helvetica", 10), bg="red", fg="white", relief="solid", width=15)
            label.grid(row=row, column=col, padx=5, pady=5)

# Modify the on_submit function to process the data after printing
def on_submit():
    subject = subject_entry.get()
    if not subject:
        messagebox.showerror("Error", "The field is empty")
        engine.say("The field is empty")
        engine.runAndWait()
        return
    data = read_csv_files(subject)
    if not data:
        messagebox.showinfo("Info", "No CSV files found in the directory.")
        engine.say("No CSV files found in the directory.")
        engine.runAndWait()
    else:
        messagebox.showinfo("Info", "Attendance calculated successfully.")
        
        print(data)  # Print the data after it's populated
        processed_data = process_data(data)  # Process the data
        print(processed_data)  # Print the processed data
        
        display_data_in_table(processed_data)  # Display the processed data in a table

# Function to create the GUI for selecting subject
def subject_choose():
    # Setup GUI
    global root
    root = tk.Tk()
    root.title("CSV Reader")
    root.configure(bg='red')  # Set background color
    root.geometry("400x200")  # Set window size

    title_label = tk.Label(root, text="CSV Reader", fg="white", bg="red", font=("Helvetica", 20))
    title_label.pack(pady=(10, 0))

    subject_label = tk.Label(root, text="Enter the subject:", fg="white", bg="red", font=("Helvetica", 12))
    subject_label.pack(pady=(20, 0))

    global subject_entry
    subject_entry = tk.Entry(root, font=("Helvetica", 12), bd=2, relief="solid", bg="white", fg="red")
    subject_entry.pack(pady=(5, 0), ipadx=20, ipady=5)

    submit_button = tk.Button(root, text="Submit", command=on_submit, font=("Helvetica", 12), bg="#16A085", fg="white", relief="raised", activebackground="grey")
    submit_button.pack(pady=(10, 0), ipadx=10, ipady=5)

    # Initialize text-to-speech engine
    global engine
    engine = pyttsx3.init()

    root.mainloop()

if __name__ == "__main__":
    subject_choose()

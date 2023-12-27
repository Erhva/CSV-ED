import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pandastable import Table, TableModel

def show_login_frame():
    frame_login.pack()

def show_csv_select_frame():
    frame_login.pack_forget()  # Hide the login frame
    frame_csv_select.pack()    # Show the CSV select frame

def show_csv_preview_frame(file_path):
    frame_csv_select.pack_forget()  # Hide the CSV select frame
    frame_csv_preview.pack()        # Show the CSV preview frame

    df = pd.read_csv(file_path)
    # Display the first few rows of the CSV file in a PandasTable
    table = Table(frame_csv_preview, dataframe=df.head())
    table.show()

def on_submit():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        show_csv_select_frame()

def on_browse():
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        file_label.config(text="File Selected: " + file_path)
        submit_button_csv.pack()  # Show the Submit button for CSV after selecting the file

def on_submit_csv():
    file_path = file_label.cget("text")[15:]  # Extracting file path from label text
    if file_path:
        show_csv_preview_frame(file_path)

# GUI setup
root = tk.Tk()
root.title("CSV Uploader")

# Login Frame
frame_login = tk.Frame(root)

# Username Entry
tk.Label(frame_login, text="Username:").pack()
username_entry = tk.Entry(frame_login)
username_entry.pack()

# Password Entry
tk.Label(frame_login, text="Password:").pack()
password_entry = tk.Entry(frame_login, show="*")
password_entry.pack()

# Submit Button
submit_button = tk.Button(frame_login, text="Submit", command=on_submit)
submit_button.pack()

# CSV Select Frame
frame_csv_select = tk.Frame(root)

# File Label
file_label = tk.Label(frame_csv_select, text="No file selected")
file_label.pack()

# Browse Button
browse_button = tk.Button(frame_csv_select, text="Browse CSV", command=on_browse)
browse_button.pack()

# Submit Button for CSV
submit_button_csv = tk.Button(frame_csv_select, text="Submit", command=on_submit_csv)

# Frame for CSV preview
frame_csv_preview = tk.Frame(root)

show_login_frame()
root.mainloop()

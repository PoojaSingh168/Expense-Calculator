import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# --- Functions ---
def add_expense():
    item = entry_item.get()
    category = combo_category.get()
    amount = entry_amount.get()
    date = datetime.now().strftime("%d-%m-%Y")

    if item == "" or category == "" or amount == "":
        messagebox.showwarning("Input Error", "Please fill all fields before adding.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount should be a number.")
        return

    # Update total
    global total_expense
    total_expense += amount
    label_total.config(text=f"Total Expense: ₹{total_expense:.2f}")

    # Add to Treeview
    tree.insert("", "end", values=(date, item, category, f"₹{amount:.2f}"))

    # Save to DataFrame
    global df
    df = pd.concat([df, pd.DataFrame([[date, item, category, amount]], columns=df.columns)], ignore_index=True)

    # Clear entry fields
    entry_item.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    combo_category.set("")


def clear_all():
    global total_expense, df
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear all records?")
    if confirm:
        for row in tree.get_children():
            tree.delete(row)
        total_expense = 0.0
        label_total.config(text="Total Expense: ₹0.00")
        df = pd.DataFrame(columns=["Date", "Item", "Category", "Amount"])


def exit_app():
    root.destroy()


def plot_category_pie():
    if df.empty:
        messagebox.showinfo("No Data", "No expenses to plot.")
        return
    data = df.groupby("Category")["Amount"].sum()
    plt.figure(figsize=(6, 6))
    plt.pie(data, labels=data.index, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
    plt.title("Expenses by Category")
    plt.show()


def plot_daily_trend():
    if df.empty:
        messagebox.showinfo("No Data", "No expenses to plot.")
        return
    data = df.groupby("Date")["Amount"].sum()
    plt.figure(figsize=(8, 5))
    plt.plot(data.index, data.values, marker='o', linestyle='-', color='blue')
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Amount (₹)")
    plt.title("Daily Expense Trend")
    plt.tight_layout()
    plt.show()


def search_expenses():
    query = entry_search.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    filtered = df[df.apply(lambda x: query in str(x["Item"]).lower()
                                     or query in str(x["Category"]).lower()
                                     or query in str(x["Date"]), axis=1)]
    for _, row in filtered.iterrows():
        tree.insert("", "end", values=(row["Date"], row["Item"], row["Category"], f"₹{row['Amount']:.2f}"))


def export_csv():
    if df.empty:
        messagebox.showinfo("No Data", "No expenses to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Exported", f"Expenses saved to {file_path}")


# --- Main Window ---
root = tk.Tk()
root.title("💰 Personal Expense Tracker")
root.geometry("900x650")
root.config(bg="#f5f7fa")

# Global variables
total_expense = 0.0
df = pd.DataFrame(columns=["Date", "Item", "Category", "Amount"])

# --- Title ---
title = tk.Label(root, text="💰 Personal Expense Tracker",
                 font=("Helvetica", 22, "bold"), bg="#f5f7fa", fg="#1f4e78")
title.pack(pady=20)

# --- Input Frame ---
frame_input = tk.Frame(root, bg="#f5f7fa")
frame_input.pack(pady=10, padx=10, fill="x")

# Item
tk.Label(frame_input, text="Item:", font=("Helvetica", 12), bg="#f5f7fa").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_item = tk.Entry(frame_input, font=("Helvetica", 12), width=25)
entry_item.grid(row=0, column=1, padx=5, pady=5)

# Category
tk.Label(frame_input, text="Category:", font=("Helvetica", 12), bg="#f5f7fa").grid(row=1, column=0, padx=5, pady=5, sticky="e")
combo_category = ttk.Combobox(frame_input, font=("Helvetica", 12), width=23, state="readonly")
combo_category['values'] = ("Food", "Transport", "Shopping", "Bills", "Entertainment", "Other")
combo_category.grid(row=1, column=1, padx=5, pady=5)

# Amount
tk.Label(frame_input, text="Amount (₹):", font=("Helvetica", 12), bg="#f5f7fa").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_amount = tk.Entry(frame_input, font=("Helvetica", 12), width=15)
entry_amount.grid(row=2, column=1, padx=5, pady=5)

# --- Buttons Frame ---
frame_buttons = tk.Frame(root, bg="#f5f7fa")
frame_buttons.pack(pady=10)

btn_add = tk.Button(frame_buttons, text="Add Expense", font=("Helvetica", 12, "bold"), bg="#007acc", fg="white", width=15, command=add_expense)
btn_add.grid(row=0, column=0, padx=10)

btn_clear = tk.Button(frame_buttons, text="Clear All", font=("Helvetica", 12, "bold"), bg="#e53935", fg="white", width=12, command=clear_all)
btn_clear.grid(row=0, column=1, padx=10)

btn_exit = tk.Button(frame_buttons, text="Exit", font=("Helvetica", 12, "bold"), bg="#333333", fg="white", width=12, command=exit_app)
btn_exit.grid(row=0, column=2, padx=10)

btn_export = tk.Button(frame_buttons, text="Export CSV", font=("Helvetica", 12, "bold"), bg="#43a047", fg="white", width=12, command=export_csv)
btn_export.grid(row=0, column=3, padx=10)

# --- Search Frame ---
frame_search = tk.Frame(root, bg="#f5f7fa")
frame_search.pack(pady=5)

tk.Label(frame_search, text="Search:", font=("Helvetica", 12), bg="#f5f7fa").pack(side="left", padx=5)
entry_search = tk.Entry(frame_search, font=("Helvetica", 12), width=30)
entry_search.pack(side="left", padx=5)
tk.Button(frame_search, text="Search", font=("Helvetica", 12, "bold"), bg="#007acc", fg="white", command=search_expenses).pack(side="left", padx=5)

# --- Treeview for Expenses ---
frame_table = tk.Frame(root)
frame_table.pack(pady=10, padx=10, fill="both", expand=True)

columns = ("Date", "Item", "Category", "Amount")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# --- Charts Frame ---
frame_charts = tk.Frame(root, bg="#f5f7fa")
frame_charts.pack(pady=10)

tk.Button(frame_charts, text="Category Pie Chart", font=("Helvetica", 12, "bold"), bg="#ff9800", fg="white", command=plot_category_pie).pack(side="left", padx=10)
tk.Button(frame_charts, text="Daily Trend Chart", font=("Helvetica", 12, "bold"), bg="#8e24aa", fg="white", command=plot_daily_trend).pack(side="left", padx=10)

# --- Total Label ---
label_total = tk.Label(root, text="Total Expense: ₹0.00", font=("Helvetica", 16, "bold"), bg="#f5f7fa", fg="#1f4e78")
label_total.pack(pady=10)

root.mainloop()

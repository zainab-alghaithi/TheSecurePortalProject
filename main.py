import tkinter as tk
from tkinter import messagebox, filedialog
from db import init_db, register_user, verify_user
from file_manager import save_file, list_files
import os

current_user = None

def open_portal():
    portal = tk.Tk()
    portal.title(f"Secure Portal - Welcome {current_user['username']} ({current_user['role']})")
    portal.geometry("600x400")

    def logout():
        portal.destroy()
        login()

    def upload_file_gui():
        try:
            file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            if file_path:
                save_file(current_user['id'], file_path)
                messagebox.showinfo("Uploaded", "File uploaded successfully.")
                view_files()
        except ValueError as ve:
            messagebox.showerror("Invalid File", str(ve))
        except Exception:
            messagebox.showerror("Error", "File upload failed. Please try again.")

    def view_files():
        files = list_files(current_user['id'], is_admin=(current_user['role'] == "admin"))
        listbox.delete(0, tk.END)
        for owner, fname in files:
            listbox.insert(tk.END, f"{owner} - {fname}")

    tk.Label(portal, text=f"Logged in as: {current_user['username']} ({current_user['role']})", font=("Arial", 14)).pack(pady=10)

    btn_upload = tk.Button(portal, text="Upload PDF File", command=upload_file_gui)
    btn_upload.pack(pady=5)

    btn_logout = tk.Button(portal, text="Logout", command=logout)
    btn_logout.pack(pady=5)

    tk.Label(portal, text="Files:", font=("Arial", 12, "bold")).pack(pady=10)

    listbox = tk.Listbox(portal, width=80)
    listbox.pack(pady=5)

    view_files()

    portal.mainloop()

def login():
    login_window = tk.Tk()
    login_window.title("Secure Portal Login")
    login_window.geometry("350x200")

    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def do_login():
        try:
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            user = verify_user(username, password)
            if user:
                global current_user
                current_user = user
                login_window.destroy()
                open_portal()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except Exception:
            messagebox.showerror("Error", "Something went wrong. Please try again.")

    def register():
        login_window.destroy()
        register_window()

    tk.Button(login_window, text="Login", command=do_login).pack(pady=10)
    tk.Button(login_window, text="Register", command=register).pack()

    login_window.mainloop()

def register_window():
    reg_window = tk.Tk()
    reg_window.title("Register New User")
    reg_window.geometry("350x250")

    tk.Label(reg_window, text="Username:").pack()
    user_entry = tk.Entry(reg_window)
    user_entry.pack()

    tk.Label(reg_window, text="Password:").pack()
    pass_entry = tk.Entry(reg_window, show="*")
    pass_entry.pack()

    tk.Label(reg_window, text="Role (admin/user):").pack()
    role_entry = tk.Entry(reg_window)
    role_entry.insert(0, "user")  # default role
    role_entry.pack()

    def do_register():
        try:
            username = user_entry.get().strip()
            password = pass_entry.get().strip()
            role = role_entry.get().strip().lower()
            if role not in ("admin", "user"):
                messagebox.showwarning("Invalid Role", "Role must be 'admin' or 'user'.")
                return

            result = register_user(username, password, role)
            if result == True:
                messagebox.showinfo("Success", "User registered.")
                reg_window.destroy()
                login()
            elif result == "weak":
                messagebox.showwarning("Weak Password",
                                       "Password must be at least 8 characters, with uppercase, lowercase, and special character.")
            else:
                messagebox.showerror("Error", "Username already exists.")
        except Exception:
            messagebox.showerror("Error", "Something went wrong. Please try again.")

    tk.Button(reg_window, text="Register", command=do_register).pack(pady=10)
    tk.Button(reg_window, text="Back to Login", command=lambda: (reg_window.destroy(), login())).pack()

    reg_window.mainloop()

if __name__ == "__main__":
    init_db()
    login()

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import app  # <== Import app.py có hàm run_app()

current_user = {"username": "", "phone": ""}

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.bg_image = Image.open("img_1.png")
        self.bg_image = self.bg_image.resize((450, 450), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self, width=450, height=450)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        content_frame = tk.Frame(self, bg='#ffffff', bd=5)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(content_frame, text="Log In", font=("Helvetica", 20, "bold"), bg='#ffffff', fg="#333")
        title.pack(pady=(20, 10))

        tk.Label(content_frame, text="Username", font=("Helvetica", 14), bg='#ffffff').pack(anchor='w', padx=20)
        self.username_entry = tk.Entry(content_frame, font=("Helvetica", 14), bd=2, relief="groove")
        self.username_entry.pack(padx=20, pady=5, fill='x')

        tk.Label(content_frame, text="Password", font=("Helvetica", 14), bg='#ffffff').pack(anchor='w', padx=20)
        self.password_entry = tk.Entry(content_frame, font=("Helvetica", 14), bd=2, relief="groove", show="*")
        self.password_entry.pack(padx=20, pady=5, fill='x')

        tk.Button(content_frame, text="Log In", font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white",
                  command=self.login).pack(pady=15, ipadx=10, ipady=5)
        tk.Button(content_frame, text="Don't have an account? Sign up", font=("Helvetica", 10, "underline"),
                  bg="#ffffff", fg="blue", bd=0, command=lambda: controller.show_page("RegisterPage")).pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username in self.controller.users and self.controller.users[username]["password"] == password:
            global current_user
            current_user["username"] = username
            current_user["phone"] = self.controller.users[username]["phone"]
            messagebox.showinfo("Successful", "Login successful!")

            self.controller.destroy()  # Đóng cửa sổ đăng nhập
            app.run_app()  # Chạy ứng dụng chính từ app.py
        else:
            messagebox.showerror("Error", "Incorrect username or password!")


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.bg_image = Image.open("img.png")
        self.bg_image = self.bg_image.resize((450, 450), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self, width=450, height=450)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        content_frame = tk.Frame(self, bg='#ffffff', bd=5)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(content_frame, text="Register", font=("Helvetica", 20, "bold"), bg='#ffffff', fg="#333")
        title.pack(pady=(20, 10))

        tk.Label(content_frame, text="Username", font=("Helvetica", 14), bg='#ffffff').pack(anchor='w', padx=20)
        self.username_entry = tk.Entry(content_frame, font=("Helvetica", 14), bd=2, relief="groove")
        self.username_entry.pack(padx=20, pady=5, fill='x')

        tk.Label(content_frame, text="Phone number", font=("Helvetica", 14), bg='#ffffff').pack(anchor='w', padx=20)
        self.phone_entry = tk.Entry(content_frame, font=("Helvetica", 14), bd=2, relief="groove")
        self.phone_entry.pack(padx=20, pady=5, fill='x')

        tk.Label(content_frame, text="Password", font=("Helvetica", 14), bg='#ffffff').pack(anchor='w', padx=20)
        self.password_entry = tk.Entry(content_frame, font=("Helvetica", 14), bd=2, relief="groove", show="*")
        self.password_entry.pack(padx=20, pady=5, fill='x')

        tk.Label(content_frame, text="Confirm Password", font=("Helvetica", 14), bg='#ffffff').pack(anchor='w', padx=20)
        self.confirm_password_entry = tk.Entry(content_frame, font=("Helvetica", 14), bd=2, relief="groove", show="*")
        self.confirm_password_entry.pack(padx=20, pady=5, fill='x')

        tk.Button(content_frame, text="Register", font=("Helvetica", 14, "bold"), bg="#2196F3", fg="white",
                  command=self.register).pack(pady=15, ipadx=10, ipady=5)
        tk.Button(content_frame, text="Already have an account? Sign in", font=("Helvetica", 10, "underline"),
                  bg='#ffffff', fg="blue", bd=0, command=lambda: controller.show_page("LoginPage")).pack()

    def register(self):
        username = self.username_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not phone or not password:
            messagebox.showerror("Error", "Please fill in all information!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Password does not match!")
            return

        if username in self.controller.users:
            messagebox.showerror("Error", "Username already exists!")
            return

        self.controller.users[username] = {"phone": phone, "password": password}
        messagebox.showinfo("Successful", "Registration successful!")
        self.controller.show_page("LoginPage")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fire Alert - Login/Register")
        self.geometry("450x450")
        self.configure(bg='#f0f2f5')
        self.users = {}

        self.container = tk.Frame(self, bg='#f0f2f5')
        self.container.pack(fill="both", expand=True)

        self.pages = {}
        for Page in (LoginPage, RegisterPage):
            page_name = Page.__name__
            frame = Page(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_page("LoginPage")

    def show_page(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()

import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import subprocess

def run_app():
    root = tk.Tk()
    root.title("Main Fire Alert App")
    root.geometry("405x500")
    tk.Label(root, text="🔥 Welcome to Fire Alert System 🔥", font=("Helvetica", 18)).pack(pady=50)
    root.mainloop()
class FireAlertApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fire Alert 114")
        self.geometry("405x500")
        self.configure(bg='white')

        self.container = tk.Frame(self, bg='white')
        self.container.pack(fill="both", expand=True)

        self.pages = {}
        for P in (HomePage, NotificationPage, AccountPage, ChooseCameraPage):
            page = P(parent=self.container, controller=self)
            self.pages[P.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.create_navbar()
        self.show_page("HomePage")

    def create_navbar(self):
        navbar = tk.Frame(self, bg='gray')
        navbar.pack(side="bottom", fill="x")

        buttons = [
            ("\U0001F3E0 Home", "HomePage"),
            ("\U0001F4F7 Camera", "ChooseCameraPage"),
            ("\U0001F514 Notification", "NotificationPage"),
            ("\U0001F464 Account", "AccountPage")
        ]

        for text, page in buttons:
            tk.Button(navbar, text=text, font=("Arial", 12), bg='orange', fg='white',
                      command=lambda p=page: self.show_page(p)).pack(side="left", expand=True, fill="both")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

    def on_closing(self):
        if "HomePage" in self.pages:
            self.pages["HomePage"].on_close()
        self.destroy()


import os  # Đừng quên import dòng này ở đầu file nếu chưa có

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.camera_index = 0
        self.cap = None

        # Hiển thị camera
        self.camera_label = tk.Label(self, bg='black')
        self.camera_label.pack(pady=10)

        # Nội dung Welcome
        self.welcome_label = tk.Label(self, text="🔥 Welcome to Fire Alert System 🔥",
                                      font=("Helvetica", 16), fg="red", bg="white")
        self.welcome_label.pack(pady=20)

        # 🔘 Nút khởi động AI báo cháy
        self.start_ai_button = tk.Button(self, text="Fire Alarm AI Start",
                                         font=("Arial", 12), bg="green", fg="white",
                                         command=self.run_fire_ai)
        self.start_ai_button.pack(pady=5)

        self.start_camera(self.camera_index)
        self.update_camera()

    def run_fire_ai(self):
        if self.cap:
            self.cap.release()
        self.controller.withdraw()  # Ẩn app chính

        try:
            # Chạy file main.py và đợi nó kết thúc
            subprocess.run(["python", "main.py"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chạy AI: {e}")
        finally:
            self.controller.deiconify()  # Hiện lại app chính sau khi AI xong
            self.start_camera(self.camera_index)

    def start_camera(self, index):
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(index)
        if not self.cap.isOpened():
            messagebox.showerror("Lỗi", f"Không thể mở camera {index}!")

    def update_camera(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame).resize((400, 300), Image.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.config(image=imgtk)
        self.after(10, self.update_camera)

    def on_close(self):
        if self.cap:
            self.cap.release()



class NotificationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        tk.Label(self, text="Thông báo", font=("Arial", 16), bg='white').pack(pady=20)
        self.notif_list = tk.Listbox(self, font=("Arial", 12), width=40, height=10)
        self.notif_list.pack(pady=10)
        self.load_notifications()

    def load_notifications(self):
        notifications = ["Phát hiện lửa tại vị trí A", "Camera mất kết nối", "Cảnh báo nhiệt độ cao"]
        for notif in notifications:
            self.notif_list.insert(tk.END, notif)


class AccountPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        tk.Label(self, text="Tài khoản", font=("Arial", 16), bg='white').pack(pady=20)
        self.username_label = tk.Label(self, text="Username: Admin", font=("Arial", 12), bg='white')
        self.username_label.pack(pady=5)
        self.phone_label = tk.Label(self, text="Phone: 123456789", font=("Arial", 12), bg='white')
        self.phone_label.pack(pady=5)

        tk.Button(self, text="Cập nhật thông tin", command=self.update_profile).pack(pady=5)
        tk.Button(self, text="Đổi mật khẩu", command=self.change_password).pack(pady=5)
        tk.Button(self, text="Đăng xuất", command=self.change_password).pack(pady=5)

    def update_profile(self):
        messagebox.showinfo("Thông báo", "Cập nhật thành công!")

    def change_password(self):
        messagebox.showinfo("Thông báo", "Mật khẩu đã được thay đổi!")


class ChooseCameraPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        tk.Label(self, text="Chọn Camera", font=("Arial", 16), bg='white').pack(pady=20)
        self.camera_var = tk.IntVar(value=0)

        for cam in range(4):
            tk.Radiobutton(self, text=f"Camera {cam}", variable=self.camera_var,
                           value=cam, font=("Arial", 12), bg='white').pack(pady=5)

        tk.Button(self, text="Xác nhận", command=self.choose_camera).pack(pady=10)

    def choose_camera(self):
        index = self.camera_var.get()
        messagebox.showinfo("Thông báo", f"Chuyển sang camera {index}")
        self.controller.pages["HomePage"].start_camera(index)


if __name__ == "__main__":
    app = FireAlertApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
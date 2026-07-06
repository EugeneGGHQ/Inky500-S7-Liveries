import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

DEFAULT_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Automobilista 2"
REQUIRED_SUBDIR = r"Vehicles\Textures\CustomLiveries\Overrides\mini_cooper"

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def validate_directory(path):
    return os.path.isdir(os.path.join(path, REQUIRED_SUBDIR))

def copy_liveries(source_repo_path, target_game_path):
    src = os.path.join(source_repo_path, REQUIRED_SUBDIR)
    dst = os.path.join(target_game_path, REQUIRED_SUBDIR)

    os.makedirs(dst, exist_ok=True)

    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        target_dir = os.path.join(dst, rel_path)
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            shutil.copy2(os.path.join(root, file), os.path.join(target_dir, file))

def run_installer():
    root = tk.Tk()
    root.title("Inky500 Season 7 Livery Installer")
    root.geometry("650x380")
    root.resizable(False, False)

    # Icon
    icon_path = resource_path("assets/gghq.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # Banner
    banner_path = resource_path("assets/inky_banner.png")
    if os.path.exists(banner_path):
        banner_img = Image.open(banner_path)
        banner_img = banner_img.resize((363, 160), Image.LANCZOS)
        banner_photo = ImageTk.PhotoImage(banner_img)

        banner_label = ttk.Label(root, image=banner_photo)
        banner_label.image = banner_photo
        banner_label.pack(pady=10)

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Select your Automobilista 2 installation directory:",
              font=("Segoe UI", 12)).pack(pady=10)

    path_var = tk.StringVar(value=DEFAULT_PATH)

    entry = ttk.Entry(frame, textvariable=path_var, width=60)
    entry.pack(pady=5)

    def browse():
        folder = filedialog.askdirectory()
        if folder:
            path_var.set(folder)

    ttk.Button(frame, text="Browse", command=browse).pack(pady=5)
    def install():
        game_path = path_var.get()

        if not validate_directory(game_path):
            messagebox.showerror(
                "Invalid Directory",
                f"The selected directory does not contain:\n{REQUIRED_SUBDIR}"
            )
            return

        repo_path = os.getcwd()

        try:
            copy_liveries(repo_path, game_path)
            messagebox.showinfo(
                "Installation Complete",
                "Liveries installed successfully.\n\n"
                "If Automobilista 2 is running, restart it to load the new liveries."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Installation failed:\n{e}")

    ttk.Button(frame, text="Install Liveries", command=install,
              style="Accent.TButton").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_installer()

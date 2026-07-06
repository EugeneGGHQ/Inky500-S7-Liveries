import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

DEFAULT_PATH = r"C:\SteamLibrary\steamapps\common\Automobilista 2"
REQUIRED_SUBDIR = r"Vehicles\Textures\CustomLiveries\Overrides\mini_cooper"

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
    root.geometry("600x250")

    tk.Label(root, text="Select your Automobilista 2 installation directory:",
             font=("Segoe UI", 12)).pack(pady=10)

    path_var = tk.StringVar(value=DEFAULT_PATH)

    entry = tk.Entry(root, textvariable=path_var, width=60)
    entry.pack(pady=5)

    def browse():
        folder = filedialog.askdirectory()
        if folder:
            path_var.set(folder)

    tk.Button(root, text="Browse", command=browse).pack(pady=5)

    def install():
        game_path = path_var.get()

        if not validate_directory(game_path):
            messagebox.showerror(
                "Invalid Directory",
                f"The selected directory does not contain:\n{REQUIRED_SUBDIR}"
            )
            return

        # Determine repo path (installer is run from repo root)
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

    tk.Button(root, text="Install Liveries", command=install,
              font=("Segoe UI", 12), width=20).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_installer()

import subprocess
import shutil
import os


def install_requirements():
    try:
        # Define the command to install requirements
        command = ["pip", "install", "-r", "requirements.txt"]

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Print the output
        print("Requirements installation output:\n", result.stdout)
        print("Requirements installation error (if any):\n", result.stderr)

    except subprocess.CalledProcessError as e:
        print("An error occurred while installing requirements:", e)
        raise


def copy_files():
    try:
        # Define source and destination paths
        img_src = "img"
        img_dest = "dist/img"
        env_src = ".env"
        env_dest = "dist/.env"

        # Copy the 'img' folder
        if os.path.exists(img_src):
            shutil.copytree(img_src, img_dest, dirs_exist_ok=True)
            print(f"Copied '{img_src}' to '{img_dest}'.")
        else:
            print(f"Source directory '{img_src}' does not exist.")

        # Copy the '.env' file
        if os.path.exists(env_src):
            shutil.copy(env_src, env_dest)
            print(f"Copied '{env_src}' to '{env_dest}'.")
        else:
            print(f"Source file '{env_src}' does not exist.")

    except Exception as e:
        print("An error occurred while copying files:", e)
        raise


def run_pyinstaller():
    try:
        # Define the command to run pyinstaller with additional data
        command = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--add-data=.env;.",
            "--add-data=img;img",
            "--icon=img/logo.ico",
            "main.py",
        ]

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Print the output
        print("PyInstaller output:\n", result.stdout)
        print("PyInstaller error (if any):\n", result.stderr)

    except subprocess.CalledProcessError as e:
        print("An error occurred while running PyInstaller:", e)


if __name__ == "__main__":
    install_requirements()
    copy_files()
    run_pyinstaller()

import os
import subprocess
import shutil
from datetime import datetime
import configparser  # Add this import
import tkinter as tk
from tkinter import filedialog, messagebox

class VideoConcatenator:
    def __init__(self, master):
        self.master = master
        self.master.title("MMBs Video Creator")
        self.sd_card_path = tk.StringVar()
        self.earliest_date_label = tk.Label(master, text="Frühester Clip: ")
        self.latest_date_label = tk.Label(master, text="Spätester Clip: ")

        # UI Elements
        tk.Label(master, text="Pfad zur SD Karte:").grid(row=0, column=0, sticky='w')
        tk.Entry(master, textvariable=self.sd_card_path, width=40).grid(row=0, column=1, padx=10)
        tk.Button(master, text="Browse", command=self.browse_sd_card).grid(row=0, column=2)

        tk.Button(master, text="Videos zusammenfuegen", command=self.combine_videos).grid(row=1, column=0, pady=10)
        tk.Button(master, text="SD Karte loeschen", command=self.confirm_delete_sd_card).grid(row=1, column=1, pady=10)

        self.earliest_date_label.grid(row=2, column=0, columnspan=3, pady=5, sticky='w')
        self.latest_date_label.grid(row=3, column=0, columnspan=3, pady=5, sticky='w')
        
    def browse_sd_card(self):
        sd_card_path = filedialog.askdirectory()
        if sd_card_path:
            self.sd_card_path.set(sd_card_path)
            self.update_date_labels()

    def get_creation_date(self, file_path):
        stat_info = os.stat(file_path)
        return datetime.fromtimestamp(stat_info.st_mtime)

    def update_date_labels(self):
        sd_card_path = self.sd_card_path.get()
        if not sd_card_path:
            return

        video_files = [f for f in os.listdir(sd_card_path) if f.endswith(('.mp4', '.avi', '.mov'))]
        if not video_files:
            return

        video_files.sort(key=lambda x: self.get_creation_date(os.path.join(sd_card_path, x)))
        earliest_date = self.get_creation_date(os.path.join(sd_card_path, video_files[0]))
        latest_date = self.get_creation_date(os.path.join(sd_card_path, video_files[-1]))

        self.earliest_date_label.config(text=f"Frühester Clip: {earliest_date}")
        self.latest_date_label.config(text=f"Spätester Clip: {latest_date}")


    def combine_videos(self):
        sd_card_path = self.sd_card_path.get()
        if not sd_card_path:
            self.show_error("Bitte richtigen Pfad zur SD Karte auswählen")
            return

        video_files = [f for f in os.listdir(sd_card_path) if f.endswith(('.mp4', '.avi', '.mov'))]
        video_files.sort(key=lambda x: self.get_creation_date(os.path.join(sd_card_path, x)))

        if not video_files:
            self.show_error("Keine Videodateien gefunden")
            return

        file_list_path = os.path.join(sd_card_path, 'file_list.txt')

        with open(file_list_path, 'w') as file_list:
            for video_file in video_files:
                file_list.write(f"file '{os.path.join(sd_card_path, video_file)}'\n")

        # Generate a unique name based on the earliest and latest date
        earliest_date = self.get_creation_date(os.path.join(sd_card_path, video_files[0]))
        latest_date = self.get_creation_date(os.path.join(sd_card_path, video_files[-1]))
        unique_name = f"output_{earliest_date.strftime('%Y%m%d')}_{latest_date.strftime('%Y%m%d')}.mp4"

        # Output file paths
        output_folder = os.path.join(os.path.expanduser("~"), "Videos", "MVC_Output")
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
        output_file = os.path.join(output_folder, unique_name)
        backup_path = self.get_backup_path()  # Fetch backup path from config
        backup_file = os.path.join(backup_path, unique_name)

        # Combine videos using FFmpeg
        self.combine_videos_ffmpeg(file_list_path, output_file)

        # Display pop-up message with output and backup paths
        self.show_info_message(f"Videos wurden erfolgreich zusammengefügt!\n\nAusgabe im Ordner:\n{output_file}\nBackup im Ordner:\n{backup_file}")

        # Save duplicate copy to the backup path
        os.makedirs(backup_path, exist_ok=True)
        shutil.copy2(output_file, backup_file)

        # Remove file_list.txt after processing
        os.remove(file_list_path)

    def combine_videos_ffmpeg(self, file_list_path, output_file):
        ffmpeg_command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', file_list_path, '-c', 'copy', output_file]
        subprocess.run(ffmpeg_command)

    def confirm_delete_sd_card(self):
        answer = messagebox.askquestion("Bestätigung", "Möchten Sie wirklich die SD Karte löschen?")
        if answer == 'yes':
            self.delete_sd_card()

    def delete_sd_card(self):
        sd_card_path = self.sd_card_path.get()
        if not sd_card_path:
            self.show_error("Bitte richtigen Pfad zur SD Karte auswählen")
            return

        video_files = [f for f in os.listdir(sd_card_path) if f.endswith(('.mp4', '.avi', '.mov'))]
        for video_file in video_files:
            os.remove(os.path.join(sd_card_path, video_file))

        self.show_info_message(f"SD Karte erfolgreich gelöscht!")

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

    def show_info_message(self, message):
        tk.messagebox.showinfo("Info", message)

    def get_backup_path(self):
    	# Read backup path from MVC.cfg configuration file
    	config_path = os.path.join(os.path.dirname(__file__), 'MVC.cfg')
    	config = configparser.ConfigParser()
    	config.read(config_path)

    	# Use the 'backup_path' key from the 'Paths' section of the configuration file
    	backup_path = config.get('Paths', 'backup_path', fallback=None)

    	if not backup_path:
        	# If the backup_path is not specified, use a default path
        	backup_path = os.path.join(os.path.expanduser("~"), "Videos", "Backup")

    	return backup_path


    def show_info_message(self, message):
        tk.messagebox.showinfo("Info", message)

def main():
    root = tk.Tk()
    app = VideoConcatenator(root)
    root.mainloop()

if __name__ == "__main__":
    main()


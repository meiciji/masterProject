'''
Controller
Master Project
9 April 2024
Mei Ying Tham
Period 6
AP CS50
'''

import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from musicDb import DatabaseManager

class MusicTracker:
    #constructor section
    def __init__(self):
        self.root = Tk()
        self.root.title("MoodTunes")
        self.root.geometry("1200x675")
        self.root.resizable(False, False)
        
        #application icon
        icon_photo = PhotoImage(file="/Users/meiyingtham/Downloads/headphones.png")
        self.root.iconphoto(True, icon_photo)

        #instantiate the database manager
        self.database_manager = DatabaseManager() 
        self.records = []
        self.current_record_index = 0 

        #frame to hold GUI elements
        self.frame = Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        #background images
        self.background_images = {
            'Happy': PhotoImage(file="/Users/meiyingtham/Downloads/yellow.png"),
            'Sad': PhotoImage(file="/Users/meiyingtham/Downloads/sad.png"),
            'Energetic': PhotoImage(file="/Users/meiyingtham/Downloads/green.png"),
            #'Relaxed': PhotoImage(file="/path/to/relaxed.png"),
            'Romantic': PhotoImage(file="/Users/meiyingtham/Downloads/pink.png"),
            #'Nostalgic': PhotoImage(file="/path/to/nostalgic.png"),
            'Angry': PhotoImage(file="/Users/meiyingtham/Downloads/red.png"),
            'Dreamy': PhotoImage(file="/Users/meiyingtham/Downloads/purple.png"),
            'Select': PhotoImage(file="/Users/meiyingtham/Downloads/blue.png")  #default
        }
        
        #initial background image
        self.background_label = Label(self.frame, image=self.background_images['Select'])
        self.background_label.image = self.background_images['Select']  # Keep a reference
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #labels
        Label(self.frame, text="ID", font=("Helvetica", 15)).place(x=170, y=130)
        Label(self.frame, text="Title", font=("Helvetica", 15)).place(x=170, y=180)
        Label(self.frame, text="Artist", font=("Helvetica", 15)).place(x=170, y=230)
        Label(self.frame, text="Genre", font=("Helvetica", 15)).place(x=170, y=280)
        Label(self.frame, text="Mood", font=("Helvetica", 15)).place(x=170, y=330)

        #etry fields
        self.entry_id = Entry(self.frame, width=30, bg="#FFFFFF", fg="black", state="readonly")
        self.entry_id.place(x=230, y=130)
        self.title_entry = Entry(self.frame, bg="#FFFFFF", width=30, fg="black")
        self.title_entry.place(x=230, y=180)
        self.artist_entry = Entry(self.frame, bg="#FFFFFF", width=30, fg="black")
        self.artist_entry.place(x=230, y=230)
        self.genre_entry = Entry(self.frame, bg="#FFFFFF", width=30, fg="black")
        self.genre_entry.place(x=230, y=280)
        self.mood_entry = Entry(self.frame, bg="#FFFFFF", width=30, fg="black")
        self.mood_entry.place(x=230, y=330)
        
        #feedback label
        self.message_label = Label(self.frame, bg="#FFFFFF", text="Press Connect to start...", fg="red", font=("Helvetica, 15"), width=50, height=2, bd=3, relief="ridge")
        self.message_label.place(x=350, y=570)
    
        #CRUD buttons
        self.add_button = Button(self.frame, text="Add Track", command=self.add_track, height=2)
        self.add_button.place(x=170, y=380)
        self.delete_button = Button(self.frame, text="Delete Track", command=self.delete_track, height=2)
        self.delete_button.place(x=310, y=380)
        self.save_button = Button(self.frame, text="Save Track", command=self.update_track, height=2)
        self.save_button.place(x=430, y=380)

        #cnnect/disconnect buttons
        Button(self.frame, text="Connect", command=self.connect_to_database, height=2).place(x=250, y=570)
        Button(self.frame, text="Disconnect", command=self.disconnect_from_database, height=2).place(x=870, y=570)
        
        #export button
        Button(self.frame, text="Export Playlist", command=self.export_playlist, height=2).place(x=750, y=400)
        
        #navigation buttons
        Button(self.frame, text="|<", command=self.first_record, height=2).place(x=170, y=440)
        Button(self.frame, text="<<", command=self.backward_record, height=2).place(x=240, y=440)
        Button(self.frame, text="<", command=self.previous_record, height=2).place(x=310, y=440)
        Button(self.frame, text=">", command=self.next_record, height=2).place(x=380, y=440)
        Button(self.frame, text=">>", command=self.forward_record, height=2).place(x=430, y=440)
        Button(self.frame, text=">|", command=self.last_record, height=2).place(x=490, y=440)

        #menu
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Connect", command=self.connect_to_database)
        self.filemenu.add_command(label="Disconnect", command=self.disconnect_from_database)
        self.filemenu.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.recordmenu = Menu(self.menubar, tearoff=0)
        self.recordmenu.add_command(label="New Track", command=self.add_track)
        self.recordmenu.add_command(label="Update Track", command=self.update_track)
        self.recordmenu.add_command(label="Delete Track", command=self.delete_track)
        self.menubar.add_cascade(label="Records", menu=self.recordmenu)

        self.navmenu = Menu(self.menubar, tearoff=0)
        self.navmenu.add_command(label="First Record", command=self.first_record)
        self.navmenu.add_command(label="Previous Record", command=self.previous_record)
        self.navmenu.add_command(label="Next Record", command=self.next_record)
        self.navmenu.add_command(label="Last Record", command=self.last_record)
        self.menubar.add_cascade(label="Navigate", menu=self.navmenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.about_popup)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.root.config(menu=self.menubar)
        
        #listbox for mood playlists 
        Label(self.frame, text="Select Mood:", font=("Helvetica", 15)).place(x=700, y=120)
        
        self.mood_var = StringVar(self.frame) #hold the current selection of the drop down menu
        self.moods = ['Select', 'Happy', 'Sad', 'Energetic', 'Relaxed', 'Romantic', 'Nostalgic', 'Angry', 'Dreamy']  #initial mood options
        self.mood_option_menu = OptionMenu(self.frame, self.mood_var, *self.moods, command=self.on_mood_selected) #create dropdown menu using strings in the list
        self.mood_option_menu.place(x=800, y=120)
        self.mood_var.set(self.moods[0])  #set default value
        
        self.track_listbox = Listbox(self.frame, width=30, height=10)
        self.track_listbox.place(x=665, y=170)

        self.root.mainloop()

    #about dialog box
    def about_popup(self):
        messagebox.showinfo("About", "MoodTunes\nMei Ying Tham\nUse this app to track your music mood-wise")

    #procedure to display feedback in label
    def display_message(self, message, success):
        if (success):
            self.message_label.config(text=message, fg="green" )
        else:
            self.message_label.config(text=message, fg="red")
    
    #connect       
    def connect_to_database(self):
        success, message = self.database_manager.connect_to_database()
        if (success):
            self.refresh_tracks() #call the procedure to update the data being displayed to the current table records
        self.display_message(message, success) #call the procedure to update feedback label with message

    #disconnect
    def disconnect_from_database(self):
        success, message = self.database_manager.disconnect_from_database()
        self.clear_record()
        self.track_listbox.delete(0, 'end')
        self.background_label.configure(image=self.background_images['Select'])
        self.background_label.image = self.background_images['Select']  # Keep a reference!
        self.display_message(message, success)

    #CREATE
    def add_track(self):
        self.clear_record()
        self.display_message("", True) #clear feedback label
        self.add_button.config(text="Commit Insertion", command=self.commit_insertion)

    def commit_insertion(self):
        #get user input from entries
        title = self.title_entry.get()
        artist = self.artist_entry.get()
        genre = self.genre_entry.get()
        mood = self.mood_entry.get().strip()
        
        if (not all([title, artist, genre, mood])):
            self.display_message("All fields must be filled out.", False)
            return

        #add to the list and dropdown if a new mood is entered
        if (mood not in self.moods):
            self.moods.append(mood)
            self.update_dropdown_menu()  #call the procedure to update the dropdown menu

        success, message = self.database_manager.add_track(title, artist, genre, mood) #call from db class
        if (success):
            self.refresh_tracks() #update the table
            self.display_current_record()
            self.display_message("Added track successfully!", True)
            self.add_button.config(text="Add Track", command=self.add_track)
        else:
            self.display_message(message, False)
            
    #DELETE
    def delete_track(self):
        track_id = self.entry_id.get()
        if (track_id):
            #confirm before deletion
            if (messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this track?")):
                success, message = self.database_manager.delete_track(track_id)
                if (success):
                    #refresh the track list
                    self.refresh_tracks()
                    self.display_message("Track deleted successfully!", True)
                    self.clear_record()
                else:
                    self.display_message(message, False)
            else:
                self.display_message("Deletion canceled", False)
        else:
            self.display_message("Please select a track to delete.", False)

    #UPDATE
    def update_track(self):
        #get user input
        track_id = self.entry_id.get()
        title = self.title_entry.get()
        artist = self.artist_entry.get()
        genre = self.genre_entry.get()
        mood = self.mood_entry.get()

        #check if all fields are filled out
        if (track_id and title and artist and genre and mood):
            success, message = self.database_manager.update_track(track_id, title, artist, genre, mood) #arguments for db method
            if (success):
                self.refresh_tracks()  #refresh list of records to show updated data
        else:
            message = "Please fill in all fields and select a valid track."
            success = False

        self.display_message(message, success)
        
    #clear entries
    def clear_record(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, END)
        self.entry_id.config(state='readonly')
        self.title_entry.delete(0, END)
        self.artist_entry.delete(0, END)
        self.genre_entry.delete(0, END)
        self.mood_entry.delete(0, END)
        
    #*****NAV*****
    def first_record(self):
        if (self.records):
            self.current_record_index = 0
            self.display_current_record()

    def previous_record(self):
        if (self.current_record_index > 0):
            self.current_record_index -= 1
            self.display_current_record()

    def next_record(self):
        if (self.current_record_index < len(self.records) - 1):
            self.current_record_index += 1
            self.display_current_record()

    def last_record(self):
        if (self.records):
            self.current_record_index = len(self.records) - 1
            self.display_current_record()

    def forward_record(self):
        if (len(self.records) > self.current_record_index + 3):
            self.current_record_index += 3
        else:
            self.last_record()
        self.display_current_record()

    def backward_record(self):
        if (self.current_record_index >= 3):
            self.current_record_index -= 3
        else:
            self.first_record()
        self.display_current_record()
    
    #procedure to update the list of records
    def refresh_tracks(self):
        success, records_or_message = self.database_manager.fetch_all_tracks()
        if (success):
            self.records = records_or_message
            self.display_current_record()
        else:
            self.display_message(records_or_message, False)

    #display record info in entries
    def display_current_record(self):
        if (self.records):
            record = self.records[self.current_record_index]
            self.entry_id.config(state='normal')
            self.entry_id.delete(0, END)
            self.entry_id.insert(0, record[0])
            self.entry_id.config(state='readonly')
            self.title_entry.delete(0, END)
            self.title_entry.insert(0, record[1])
            self.artist_entry.delete(0, END)
            self.artist_entry.insert(0, record[2])
            self.genre_entry.delete(0, END)
            self.genre_entry.insert(0, record[3])
            self.mood_entry.delete(0, END)
            self.mood_entry.insert(0, record[4])
        else:
            self.clear_record()
    
    #procedure when user selects a mood
    def on_mood_selected(self, mood=None): #passes with or without a specific mood
        #handles mood selection change
        self.mood_var.get() #get currently selected value in dropdown menu
        
        #update the background image
        if (mood in self.background_images):
            self.background_label.configure(image=self.background_images[mood])
            self.background_label.image = self.background_images[mood]  #keep reference
            
        success, tracks = self.database_manager.fetch_tracks_by_mood(mood) #call db method
        self.track_listbox.delete(0, 'end')
        if (success):
            self.track_listbox.delete(0, END) #clear the listbox for following displays
            for track in tracks:
                self.track_listbox.insert(END, track) #each fetched track is inserted into listbox
        else:
            self.display_message(tracks, False)
    
    #procedure to select tracks by mood from db    
    def fetch_tracks_by_mood(self, mood):
        return self.database_manager.fetch_tracks_by_mood(mood)
    
    #procedure to export listbox playlist 
    def export_playlist(self):
        #get the selected songs from listbox
        selected_songs = self.track_listbox.get(0, END)

        #open a file dialog to choose the export location
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        
        if (file_path):  #ensure the file path was chosen
            #open the file in write mode
            file = open(file_path, "w")
            
            #write each song to the file
            for song in selected_songs:
                file.write(song + "\n")
            file.close()
            
            webbrowser.open("https://www.tunemymusic.com", new=1) #open website after saving file to a new window
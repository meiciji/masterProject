'''
Database
Master Project
9 April 2024
Mei Ying Tham
Period 6
AP CS50
'''

import mysql.connector

class DatabaseManager:
    def __init__(self):
        #initialization variables
        self.connection = None

    #connect to db
    def connect_to_database(self):
        if (not self.connection):
            try:
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="thamfamily0",
                    db="moodtunes",
                )
                return True, "Connected to the database."
            except mysql.connector.Error as err:
                return False, f"Error: {err}"
        return False, "Already connected to the database."

    #disconnect
    def disconnect_from_database(self):
        if (self.connection):
            try:
                self.connection.close()
                self.connection = None #reset
                return True, "Disconnected from the database."
            except Exception as err:
                return False, f"Failed to disconnect: {err}"
        return False, "Already disconnected from the database."

    #CREATE
    def add_track(self, title, artist, genre, mood):
        if (self.connection):
            #check if all input fields are filled
            if (title.strip() and artist.strip() and genre.strip() and mood.strip()):
                try:
                    #creating cursor object for db
                    cursor = self.connection.cursor()
                    query = "INSERT INTO tracks (title, artist, genre, mood) VALUES (%s, %s, %s, %s)"
                    #data to be inserted into db
                    data = (title, artist, genre, mood)
                    #execute the query with the data
                    cursor.execute(query, data)
                    self.connection.commit()
                    cursor.close()
                    return True, "Track added successfully!"
                except mysql.connector.Error as err:
                    return False, f"Failed to add track: {err}"
            return False, "Please fill in all fields."
        return False, "Not connected to the database."

    #DELETE
    def delete_track(self, track_id):
        if (self.connection):
            try:
                cursor = self.connection.cursor()
                #deletion based off selected ID
                query = "DELETE FROM tracks WHERE id = %s"
                data = (track_id,)
                cursor.execute(query, data)
                self.connection.commit()
                cursor.close()
                return True, "Track deleted successfully!"
            except mysql.connector.Error as err:
                return False, f"Failed to delete track: {err}"
        return False, "Not connected to the database."

    #UPDATE
    def update_track(self, track_id, title, artist, genre, mood):
        if (self.connection):
            try:
                cursor = self.connection.cursor()
                #query to update the record with the new entries
                query = "UPDATE tracks SET title = %s, artist = %s, genre = %s, mood = %s WHERE id = %s"
                data = (title, artist, genre, mood, track_id)
                cursor.execute(query, data)
                self.connection.commit()
                cursor.close()
                return True, "Track updated successfully!"
            except mysql.connector.Error as err:
                return False, f"Failed to update track: {err}"
        return False, "Not connected to the database."

    #READ
    def fetch_all_tracks(self):
        if (self.connection):
            try:
                cursor = self.connection.cursor()
                #query to select all records ordered by ID in ascending order
                cursor.execute("SELECT * FROM tracks ORDER BY id ASC")
                #get all records from db
                records = cursor.fetchall()
                cursor.close()
                return True, records
            except mysql.connector.Error as err:
                return False, f"Error fetching tracks: {err}"
        return False, "Not connected to the database."

    #filter records by mood
    def fetch_tracks_by_mood(self, mood):
        if (self.connection):
            try:
                cursor = self.connection.cursor()
                #query to select records by mood in ABC order
                query = "SELECT title FROM tracks WHERE mood = %s ORDER BY title ASC"
                cursor.execute(query, (mood,))
                titles = cursor.fetchall()  #get only the titles
                cursor.close()
                return True, [title[0] for title in titles]  # Unpack titles from tuples
            except mysql.connector.Error as err:
                return False, f"Error fetching tracks by mood: {err}"
        return False, "Not connected to the database."
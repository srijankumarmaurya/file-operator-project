from datetime import datetime
import os  # Added to allow physical file deletion

print("Welcome to the Personal Journal Manager!")
print()


class JournalManager:

    def __init__(self, filename="filename.txt"):
        self.filename = filename
        # Automatically create the file on startup if it doesn't exist
        self.creating_file()

    def creating_file(self):
        try:
            with open(self.filename, "x") as file:
                pass
        except FileExistsError:
            pass  # File already exists, which is fine

    def add_entry(self):
        entry = input("Enter data in your journal: ")
        if not entry.strip():
            print("Please enter a valid entry.")
            return

        # Capture the exact, current time right now
        samaye = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(self.filename, "a") as file:
                # Keep entry and time together so search picks up both
                file.write(f"[{samaye}] {entry}\n")
                print("Entry saved successfully!")
                print()
        except ValueError:
            print("An error occurred while adding the entry.")
            print()

    def view_entries(self):
        try:
            if not os.path.exists(self.filename):
                print(
                    "File not found. It may have been deleted. Please restart or add an entry to recreate it."
                )
                print()
                return

            with open(self.filename, "r") as file:
                entries = file.readlines()
                if entries:
                    print("--- Journal Entries ---")
                    for entry in entries:
                        print(entry.strip())
                    print("-----------------------")
                    print()
                else:
                    print("No entries found.")
                    print()

        except FileNotFoundError:
            print("The file was not found.")
        
            print()

    def search_entry(self):
        if not os.path.exists(self.filename):
            print("File not found. There is nothing to search.")
            print()
            return

        keyword = input("Enter the text or word you want to search: ")
        try:
            with open(self.filename, "r") as file:
                entries = file.readlines()
                # Matches if the keyword is anywhere in the timestamp or the entry text
                found_entries = [
                    entry for entry in entries if keyword.lower() in entry.lower()
                ]

                if found_entries:
                    print()
                    print("Entries found:")
                    for entry in found_entries:
                        print(entry.strip())
                else:
                    print("No entries found with the given keyword.")
                print()

        except FileNotFoundError:
            print("The file was not found.")
        
            print()

    def delete_whole_file(self):
        # Safety check to protect user data from accidental clicks
        
        confirm = (input("Are you absolutely sure you want to permanently delete the entire file? (yes/no): ").strip().lower())
        
        if confirm != "yes":
            print("Deletion cancelled.")
            print()
            return

        try:
            if os.path.exists(self.filename):
                os.remove(self.filename)  # Physically deletes the file
                print(f"The file '{self.filename}' has been completely deleted from your system.")
                print()
            else: 
                print("File not found. There is nothing to delete.")
                print()
        except PermissionError:
            print("An error occurred while deleting the file. Please ensure you have the necessary permissions.")
            print()


# Initializing the manager ONCE outside the loop
journal_manager = JournalManager()

while True:
    print("Please select an option:")
    print("1. Add a new entry")
    print("2. View all the entries")
    print("3. Search for an entry")
    print("4. Delete the whole file")
    print("5. Exit")

    raw_option = input("Enter the option number from the above: ")
    print() 
    if not raw_option.isdigit():
        print("Please enter a valid option number from 1-5 only.")
        print()
        continue

    option = int(raw_option)
    if option == 1:
        # If they deleted the file earlier, recreate it when they try to write a new entry
        journal_manager.creating_file()
        journal_manager.add_entry()
    elif option == 2:
        journal_manager.view_entries()
    elif option == 3:
        journal_manager.search_entry()
    elif option == 4:
        journal_manager.delete_whole_file()
    elif option == 5:
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Please enter a number between 1 and 5.")
        print()
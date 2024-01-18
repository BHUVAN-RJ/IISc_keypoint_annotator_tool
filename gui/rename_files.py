import os

def rename_files(folder_path):
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    files = os.listdir(folder_path)
    files.sort()  # Ensure the files are sorted in alphabetical order

    new_name_counter = 80000

    for old_name in files:
        old_path = os.path.join(folder_path, old_name)

        # Get the file extension
        _, file_extension = os.path.splitext(old_name)

        # Construct the new name with the incrementing order
        new_name = f"{new_name_counter}{file_extension}"
        new_path = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(old_path, new_path)

        new_name_counter += 1

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    rename_files(folder_path)
    print("Files renamed successfully.")
from organizer.operations import organize_folder

def main():
    """
    Prompts the user for a folder path and initiates the organization process.
    """
    try:
        folder_to_organize = input("Enter the full path of the folder you want to organize: ")
        if folder_to_organize:
            organize_folder(folder_to_organize)
        else:
            print("No path entered. Exiting.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

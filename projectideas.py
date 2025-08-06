import pandas as pd
import re

def process_and_save(project_data, output_file):
    """
    Processes the project data and saves it to a file.
    """
    with open(output_file, 'a') as output:
        for project in project_data:
            # Clean the data and validate non-empty fields
            cleaned_data = [re.sub(r'\s+', ' ', field) for field in project]
            if all(cleaned_data):  # Ensure no fields are empty
                formatted_project = "Project Idea: {0} Description: {1} Tools Used: {2}\n".format(*cleaned_data)
                output.write(formatted_project)
    print(f"Formatted project ideas saved to {output_file}")

def load_from_file():
    """
    Loads project data from a CSV file.
    """
    file_path = input("Enter the file path for the CSV: ").strip()
    try:
        df = pd.read_csv(file_path)
        project_data = df[['Project Title :-', 'Description of Project :-', 'Tools Used :-']].values.tolist()
        return project_data
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

def input_from_user():
    """
    Allows the user to input project data manually.
    """
    project_data = []
    print("Enter project details (leave any field empty to stop):")
    while True:
        title = input("Project Title: ").strip()
        description = input("Description of Project: ").strip()
        tools = input("Tools Used: ").strip()
        if not title or not description or not tools:
            break
        project_data.append([title, description, tools])
    return project_data

def main():
    output_file = 'p.txt'
    while True:
        print("\nMenu:")
        print("1. Load project data from file")
        print("2. Enter project data manually")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        
        if choice == '1':
            project_data = load_from_file()
            if project_data:
                process_and_save(project_data, output_file)
        elif choice == '2':
            project_data = input_from_user()
            if project_data:
                process_and_save(project_data, output_file)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

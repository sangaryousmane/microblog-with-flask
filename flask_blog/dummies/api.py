from requests import get, exceptions
import csv
import json


def get_employee_todo_data(employee_id):
    """
    Retrieves TODO list data for an employee and returns the relevant information.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        tuple: (employee_name, todos_data)
            employee_name (str): The name of the employee.
            todos_data (list): A list of task dictionaries containing 'title' and 'completed' fields.
    """

    base_url = "https://jsonplaceholder.typicode.com/"
    employee_url = f"{base_url}users/{employee_id}"
    todos_url = f"{base_url}todos?userId={employee_id}"

    try:
        # Fetch employee data
        employee_response = get(employee_url)
        employee_data = employee_response.json()

        # Fetch TODO list data
        todos_data = get(todos_url).json()

        return employee_data["name"], todos_data

    except exceptions.RequestException as e:
        return None, None  # Return None values on error


def get_employee_todo_data_and_export_csv(employee_id):
    """
    Retrieves TODO list data for an employee, prints progress summary, and exports data to a CSV file.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        None
    """
    employee_name, todos_data = get_employee_todo_data(employee_id)

    if employee_name and todos_data:
        # Create CSV file
        file_name = f"{employee_id}.csv"
        with open(file_name, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            for task in todos_data:
                csv_writer.writerow([
                    employee_id,
                    employee_name,
                    "True" if task["completed"] else "False",
                    task["title"]])
    else:
        print("Is the ID correct?")


def get_employee_todo_data_and_export_json(employee_id):
    """
    Retrieves TODO list data for an employee, prints progress summary, and exports data to a JSON file.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        None
    """

    employee_name, todos_data = get_employee_todo_data(employee_id)

    if employee_name and todos_data:
        json_data = {
            "USER_ID": [{
                "task": task["title"],
                "completed": task["completed"],
                "username": employee_name
            } for task in todos_data
            ]}
    else:
        print("Is the ID correct?")

    file_name = f"{employee_id}.json"
    with open(file_name, "w") as jsonfile:
        json.dump(json_data, jsonfile, indent=4)


def get_all_employees_todo_data_and_export_json():
    """
    Retrieves TODO list data for all employees, prints progress summaries, and exports data to a JSON file.

    Returns:
        None
    """

    base_url = "https://jsonplaceholder.typicode.com/"
    users_url = f"{base_url}users"

    try:
        # Fetch all employee IDs
        employee_ids = [user["id"] for user in get(users_url).json()]

        # Collect TODO data for each employee
        all_employee_data = {}
        for employee_id in employee_ids:
            # Fetch and print progress for individual employee
            employee_name, todos_data = get_employee_todo_data(employee_id)  # Reuse function from task #0

            # Format task data for JSON
            employee_task_data = [
                {
                    "username": employee_name,  # Access employee name from previous fetch
                    "task": task["title"],
                    "completed": task["completed"]
                } for task in todos_data
            ]

            # Add employee data to the main dictionary
            all_employee_data[employee_id] = employee_task_data

        # Write combined JSON data to file
        file_name = "todo_all_employees.json"
        with open(file_name, "w") as jsonfile:
            json.dump(all_employee_data, jsonfile, indent=4)
        print("Done")

    except exceptions.RequestException as e:
        print(f"Error fetching data: {e.errno}")


print(get_all_employees_todo_data_and_export_json())


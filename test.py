import requests
import json
import http.client
import base64

def mess(id):
    headers = {
        'authorization' : 'NzUyNjM4NjQxMDg3NDQ3MDkw.YcT27A.7sBp10wWIQx9CC0JOHFSyPMdWGA'
    }
    r = requests.get(f'https://discord.com/api/v10/channels/{id}/messages', headers=headers)
    js = json.loads(r.text)
    print(js)

def get_access_token(Client, code, _redirect_uri):
    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": Client._id,
        "client_secret": Client._client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": _redirect_uri,
        "scope": "identify"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=data, headers=headers)
    response_json = response.json()
    print(response_json)
    access_token = response_json["access_token"]
    return (f"Access token: {access_token}")

class ClientModel:
    def __init__(self, token:str,client_secret:str, id:int) -> None:
        self._client_secret = client_secret
        self._token = token
        self._id = id
        self.conn = http.client.HTTPSConnection('discord.com')

    def get_access_token(self, code, _redirect_uri):
        token_url = "https://discord.com/api/oauth2/token"
        data = {
            "client_id": self._id,
            "client_secret": self._client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": _redirect_uri,
            "scope": "identify"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(token_url, data=data, headers=headers)
        response_json = response.json()
        print(response_json)
        access_token = response_json["access_token"]
        return response_json
    def refresh_access_token(self, refresh_token):
        params = {
        "client_id": self._id,
        "client_secret": self._client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "identify"
        }

        response = requests.post("https://discord.com/api/oauth2/token", data=params)

        if response.status_code == 200:
            response_json = response.json()
            new_access_token = response_json["access_token"]
            new_refresh_token = response_json["refresh_token"]
            return (f"data: {new_access_token}, {new_refresh_token} ")
        else:
            return (f"Error: {response.status_code}")
        

    def get_discord_access_token(self, redirect_uri: str, code: str) -> str:
        token_url = 'https://discord.com/api/oauth2/token'

        auth_string = f'{self._id}:{self._client_secret}'
        auth_bytes = auth_string.encode('ascii')
        auth_base64 = base64.b64encode(auth_bytes)
        auth_header = f'Basic {auth_base64.decode("ascii")}'

        conn = http.client.HTTPSConnection('discord.com')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': auth_header
        }
        payload = f'grant_type=authorization_code&code={code}&redirect_uri={redirect_uri}&scope=identify%20email'
        conn.request('POST', '/api/oauth2/token', payload, headers)

        response = conn.getresponse()
        data = response.read()
        json_data = json.loads(data)
        access_token = json_data['access_token']

        return access_token
    

class BearerClient:
    def __init__(self, access_token : str) -> None:
        self.token = access_token
        self.conn = http.client.HTTPSConnection('discord.com')
    def get_user_data(self) -> dict:
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        self.conn.request('GET', '/api/users/@me', headers=headers)

        response = self.conn.getresponse()
        data = response.read()
        user_data = json.loads(data)

        return user_data
    def get_user_guilds(self) -> list:
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        self.conn.request('GET', '/api/users/@me/guilds', headers=headers)

        response = self.conn.getresponse()
        data = response.read()
        guilds = json.loads(data)

        return guilds
    
import socket
import ssl

def request_access_token(client_id: str, client_secret: str, code: str, redirect_uri: str) -> dict:
    host = "discord.com"
    path = "/api/oauth2/token"
    port = 443

    data = f"client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code&code={code}&redirect_uri={redirect_uri}"
    request = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(data)}\r\nConnection: close\r\n\r\n{data}"

    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            ssock.sendall(request.encode())

            response = b""
            while True:
                data = ssock.recv(1024)
                if not data:
                    break
                response += data

    response_text = response.decode().split("\r\n\r\n", 1)[-1]
    # start_pos = response_text.find('{')
    # end_pos = response_text.rfind('}') + 1

    # cleaned_text = response_text[start_pos:end_pos]

    response_json = json.loads(response_text)
    return response_json
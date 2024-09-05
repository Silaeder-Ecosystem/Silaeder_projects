import json
import http.client
import requests

def parse_data(field):
    file = open('config.json')
    data = json.load(file)[field]
    file.close()
    return data

def add_field_to_config(a, b):
    with open('config.json', 'r') as file:
        config = json.load(file)
    config[a] = b
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

def recreate_auth0_token():
    auth0 = http.client.HTTPSConnection(parse_data('AUTH0_DOMAIN'))
    payload = "{\"client_id\":\"%s\",\"client_secret\":\"%s\",\"audience\":\"https://%s/api/v2/\",\"grant_type\":\"client_credentials\"}" % (parse_data('AUTH0_API_CLIENT_ID'), parse_data('AUTH0_API_CLIENT_SECRET'), parse_data('AUTH0_DOMAIN'))
    headers = { 'content-type': "application/json" }

    auth0.request("POST", "/oauth/token", payload, headers)
    res = auth0.getresponse()
    response_data = str(res.read().decode("utf-8"))
    token_data = json.loads(response_data)
    add_field_to_config("AUTH0_TOKEN", token_data['access_token'])
    print('token recreated')
    return token_data['access_token']

def get_user_by_username(username, token=parse_data("AUTH0_TOKEN")):
    url = f"https://{parse_data('AUTH0_DOMAIN')}/api/v2/users?q={username}"
    payload = {}
    headers = {
      'Accept': 'application/json',
      "Authorization": f"Bearer {token}"
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.json()
    if type(res) != list:
        return get_user_by_username(username, token=recreate_auth0_token())
    return res

def check_user_is_exist(username, token=parse_data("AUTH0_TOKEN")):
    res = get_user_by_username(username)
    for i in res:
        if i['username'] == username:
            return True
    return False

def change_username(old_username, new_username, token=parse_data("AUTH0_TOKEN")):
    users = get_user_by_username(old_username)
    user = None
    for i in users:
        if i['username'] == old_username:
            user = i
            break
    url = f"https://{parse_data('AUTH0_DOMAIN')}/api/v2/users/auth0%7C{user['user_id'][6:]}"
    payload = json.dumps({
        "username": new_username
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      "Authorization": f"Bearer {token}"
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)
    res = response.json()
    return res

def update_user_password(username, password, token=parse_data("AUTH0_TOKEN")):
    users = get_user_by_username(username)
    user = None
    for i in users:
        if i['username'] == username:
            user = i
            break
    url = f"https://{parse_data('AUTH0_DOMAIN')}/api/v2/users/auth0%7C{user['user_id'][6:]}"
    payload = json.dumps({
        "password": password
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      "Authorization": f"Bearer {token}"
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    res = response.json()
    return res
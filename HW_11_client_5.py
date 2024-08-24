import requests

API_URL = 'http://localhost:4000'

def fetch_token():
    response = requests.post(f'{API_URL}/create-token')
    return response.json().get('token')

def greet(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{API_URL}/welcome', headers=headers)
    print(response.text)

def execute_command(token, instruction):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{API_URL}/command', json={'instruction': instruction}, headers=headers)
    print(response.text)

if __name__ == '__main__':
    token = fetch_token()
    if token:
        greet(token)
        execute_command(token, 'start')

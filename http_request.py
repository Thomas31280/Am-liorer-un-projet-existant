import requests


class Requests:

    @classmethod
    def get_data_from_api(cls, request_url):

        api_response = requests.get(request_url)
        print(api_response)
        return api_response.json()

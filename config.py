import configparser

config = configparser.ConfigParser(interpolation=None)
config.read('credentials.conf')

TEST_LLMs_API_ACCESS_TOKEN = config.get('TEST', 'access_token')
TEST_LLMs_REST_API_URL = config.get('TEST', 'rest_api_url')


import os

AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID', "")
AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET', "")

AZURE_GRAPH_API_BASE_URL = 'https://graph.microsoft.com'
AZURE_GRAPH_API_VERSION = 'v1.0'

AZURE_TOKEN_URL = 'https://login.microsoftonline.com/unicef.org/oauth2/token'

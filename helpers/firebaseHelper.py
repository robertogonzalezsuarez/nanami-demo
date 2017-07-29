import logging

from environment.environment import SERVICE_ACCOUNT_JSON, FIREBASE_SCOPE
from oauth2client.service_account import ServiceAccountCredentials


def get_credentials(user_mail=''):
    """
    Args:
        user_mail: mail of the user to impersonate, if any.

    Returns:
        Credentials object with the requested credentials, delegated from the user_email if any.

    """
    # Normal call to get credentials from Service Account
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_JSON, scopes=FIREBASE_SCOPE)

    return credentials.get_access_token().access_token

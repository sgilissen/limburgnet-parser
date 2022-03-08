"""
    File name: parser.py
    Author: Steve Gilissen
    Date created: 07/03/2022
    Date last modified: 08/03/2022
    Python Version: 3.8+
"""

__author__ = "Steve Gilissen"
__credits__ = ["Steve Gilissen"]
__license__ = "GPLv3"
__version__ = "0.0.1"
__status__ = "Development"

import requests
import datetime

limnet_base_url = 'https://limburg.net/api-proxy/public/'


class APIParser:
    def __init__(self):
        self.base_url = limnet_base_url

    def search_municipality(self, municipality):
        """
        Search the municipality specified
        :param municipality: Name of the municipality, string
        :return: Municipalities found, as a JSON array
        """
        endpoint = 'afval-kalender/gemeenten/'
        r = requests.get(f'{self.base_url}{endpoint}search?query={municipality}')

        # Try if we get a 200 response. If not, return error
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return {'Error': e}

        # If we get a 200 response, return a JSON object
        return r.json()

    def search_street(self, street, municipality_id):
        """
        Search for the given street name, filtered by the municipality ID
        :param street: Name of the street, as a string
        :param municipality_id: Municipality ID to filter by, as a string
        :return: Streets found, as a JSON array
        """
        endpoint = 'afval-kalender/gemeente/'

        r = requests.get(f'{self.base_url}{endpoint}{municipality_id}/straten/search?query={street}')
        # Try if we get a 200 response. If not, return error
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return {'Error': e}

        # If we get a 200 response, return a JSON object
        return r.json()

    def search_housenumber(self, house_number, street_id):
        """
        Search for the house number, filtered by the street ID, which can be found using the search_street function
        :param house_number: Number to search
        :param street_id: ID of the street to filter by, as a string
        :return: Numbers found, as a JSON array
        """
        endpoint = 'afval-kalender/straat/'

        r = requests.get(f'{self.base_url}{endpoint}{street_id}/huisnummers/search?query={house_number}')
        # Try if we get a 200 response. If not, return error
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return {'Error': e}

        # If we get a 200 response, return a JSON object
        return r.json()

    def fetch_next_collection(self, municipality_id, street_id, house_num, house_suffix=''):
        """
        Fetches the upcoming collection dates and fractions, filtered by the given municipality ID, street ID,
        house number and house suffix (optional)
        :param municipality_id: The ID of the municipality
        :param street_id: the ID of the street
        :param house_num: The house number
        :param house_suffix: (Optional) house suffix
        :return: The next collection date and fractions, as a JSON array
        """
        endpoint = 'volgende-afval-ophaling/'

        r = requests.get(f'{self.base_url}{endpoint}'
                         f'{municipality_id}?straatNummer={street_id}'
                         f'&huisNummer={house_num}&toevoeging={house_suffix}')

        # Try if we get a 200 response. If not, return error
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return {'Error': e}

        # If we get a 200 response, return a JSON object
        return r.json()

    def fetch_month_calendar(self, municipality_id, street_id, house_number, house_suffix=''):
        """
        Fetch the collection calendar for the current month
        :param municipality_id: the ID of the municipality
        :param street_id: the street ID
        :param house_number: the house number
        :param house_suffix: (Optional) house suffix
        :return: Collection calendar, as a JSON array
        """
        endpoint = 'kalender/'

        current_datetime = datetime.datetime.now()
        # Endpoint expects YYYY-M, so we'll need to format it that way
        formatted_date = f'{current_datetime.year}-{current_datetime.month}'

        r = requests.get(f'{self.base_url}{endpoint}/{municipality_id}/{formatted_date}?straatNummer={street_id}'
                         f'&huisNummer={house_number}&toevoeging={house_suffix}')

        # Try if we get a 200 response. If not, return error.
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return {'Error': e}

        data = r.json()

        # Build new dictionary with the data we need. We'll use a dictionary comprehension for readability.
        calendar = {
            event['date']:
                {
                    'category': event['category'],
                    'detail_url': event['detailUrl']
                } for event in data['events']}

        # Return the dictionary
        return calendar

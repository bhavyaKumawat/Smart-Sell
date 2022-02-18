import os
import asyncio
import logging
import requests
from typing import Dict
from bs4 import BeautifulSoup

logger = logging.getLogger()


url = os.environ["lookup_url"]
SOAPAction = os.environ["SOAPAction"]


# async def batch_get_tills(tokens_dict: Dict) -> Dict:
#     try:
#         till_numbers = {}
#         tills = await asyncio.gather(*(get_till_numbers(tokens['LocationToken'], tokens['AccessToken']) for _, tokens in tokens_dict.items()))
#         await asyncio.gather(*(parse_xml(data, till_numbers) for data in tills))
#
#         return till_numbers
#     except Exception as ex:
#         logger.exception(f'Exception while getting Till Number: {ex!r}')


async def get_tills(tokens: Dict) -> Dict:
    try:
        till_numbers = {}
        tills = get_till_numbers(tokens['LocationToken'], tokens['AccessToken'])
        await parse_xml(tills, till_numbers)
        return till_numbers
    except Exception as ex:
        logger.exception(f'Exception while getting Till Number: {ex!r}')


async def get_till_numbers(location_token: str, access_token: str) -> str:
    try:
        global url, SOAPAction
        url = url

        payload = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
        <s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">
        <s:Body><GetTills xmlns=\"http://www.brinksoftware.com/webservices/sales/v2\">
        <request xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\">
        <BusinessDate>2021-12-08T00:00:00</BusinessDate>
        </request>
        </GetTills></s:Body></s:Envelope>"""

        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'AccessToken': access_token,
            'LocationToken': location_token,
            'SOAPAction': SOAPAction
        }

        logger.debug("Making API Calls to to get employee details...")
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.ok:
            return response.text

    except Exception as ex:
        logger.exception(f'Exception while getting Employee Details from Till Number: {ex!r}')


async def parse_xml(data: str, till_numbers: Dict):
    try:
        xml = BeautifulSoup(data, 'xml')
        for item in xml.find_all('Till'):
            till_numbers[int(item.find('Number').getText())] = {'EmployeeId': item.find('EmployeeId').getText()}
    except Exception as ex:
        logger.exception(f'Exception while Parsing XML...: {ex!r}')

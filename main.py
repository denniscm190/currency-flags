from selenium import webdriver
import json
import requests
import os


def get_currency_symbols():
    """
    Get currency symbols
    :return:
    """

    driver = webdriver.Firefox()
    driver.get('https://1forge.com/currency-list')
    elements = driver.find_elements_by_class_name('wide-column')
    currencies = {}
    for currency in elements:
        splitted_currency = currency.text.split(' - ')
        currency_values = {'name': splitted_currency[1], 'flag': splitted_currency[0][:2]}
        currencies[splitted_currency[0]] = currency_values

    with open('currencies.json', 'w') as f:
        json.dump(currencies, f)


def get_flags():
    """
    Given the currency symbol previously obtained, download country flags for every currency
    :return:
    """

    with open('currencies.json') as f:
        currencies = json.load(f)
        for currency_symbol in currencies.keys():
            country_flag = currencies[currency_symbol]['flag']
            response = requests.get('https://flagcdn.com/h240/' + country_flag.lower() + '.png')
            if response.status_code == 200:
                file = open('src/' + country_flag + '.png', 'wb')
                file.write(response.content)
                file.close()
            else:
                print('Failed currency symbol: ' + currency_symbol + ' with code: ' + str(response.status_code))


def check_all_flags():
    """
    Check if there are flags for every currency
    :return:
    """

    with open('currencies.json') as f:
        currencies = json.load(f)
        flags_in_json = []
        for currency in currencies.keys():
            flags_in_json.append(currencies[currency]['flag'])

        flags = os.listdir('src/')
        for flag in flags:
            if flag.split('.')[0] not in flags_in_json:
                print(flag)


if __name__ == '__main__':
    get_currency_symbols()
    get_flags()
    check_all_flags()

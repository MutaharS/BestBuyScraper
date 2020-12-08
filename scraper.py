import requests
import json
import boto3
from datetime import datetime
import time
import codecs
 
URL = 'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=961%7C973%7C600%7C958%7C994%7C952%7C705%7C242%7C941%7C796%7C915%7C929%7C13%7C701%7C992&postalCode=V3L&skus=15166285'
 
headers = {
    'authority': 'www.bestbuy.ca',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4159.2 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3060-ti-8gb-gddr6-video-card/15166285',
    'accept-language': 'en-US,en;q=0.9'
}
 
def main():
    quantity = 0
    attempt = 0
 
    while (quantity < 1):
        response = requests.get(URL, headers=headers)
        #response_formatted = json.load(codecs.open(response.content, 'r', 'utf-8-sig'))
        response_formatted = json.loads(response.content.decode('utf-8-sig'))
        
        quantity = response_formatted['availabilities'][0]['shipping']['quantityRemaining']
 
        if (quantity < 1):
            #Out Of stock
            print('Time=' + str(datetime.now()) + "- Attempt=" + str(attempt))
            attempt += 1
            time.sleep(5)
        else:
            print('Hey its in stock! Quantity=' + str(quantity))
            publish(quantity)
 
 
def publish(quantity):
    arn = 'arn:aws:sns:insert arn here'
    sns_client = boto3.client(
        'sns',
        aws_access_key_id='accesskey',
        aws_secret_access_key='secretkey',
        region_name='us-east-1'
    )
 
    response = sns_client.publish(TopicArn=arn, Message='Its in stock! Quantity=' + str(quantity))
    print(response)
 
main()
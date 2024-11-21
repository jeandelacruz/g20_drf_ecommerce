from django.conf import settings

from requests import post, get


class MercadopagoClient:
    def __init__(self):
        self.access_token = settings.MERCADOPAGO_ACCESS_TOKEN
        self.base_url = 'https://api.mercadopago.com'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

    def create_preferences(self, payer, products, order_id):
        url = f'{self.base_url}/checkout/preferences'
        body = {
            'payer': payer,
            'items': products,
            'external_reference': order_id
        }
        response = post(url, json=body, headers=self.headers)
        return response.json()

    def get_payment_by_id(self, payment_id):
        url = f'{self.base_url}/v1/payments/{payment_id}'
        response = get(url, headers=self.headers)
        return response.json()

    def get_merchant_order_by_id(self, merchant_order_id):
        url = f'{self.base_url}/merchant_orders/{merchant_order_id}'
        response = get(url, headers=self.headers)
        return response.json()

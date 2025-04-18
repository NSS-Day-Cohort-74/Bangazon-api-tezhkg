import json
from rest_framework import status
from rest_framework.test import APITestCase
import datetime

class OrderTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Steve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a product category
        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        # Create a product
        url = "/products"
        data = { "name": "Kite", "price": 14.99, "quantity": 60, "description": "It flies high", "category_id": 1, "location": "Pittsburgh" }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Create a payment type
        url='/paymenttypes'
        data ={
            "merchant_name": "Amex",
            "account_number": "000000000000",
            "expiration_date": "2023-12-12",
            "create_date": "2020-12-12"
        }
        self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_product_to_order(self):
        """
        Ensure we can add a product to an order.
        """
        # Add product to order
        url = "/profile/cart"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get cart and verify product was added
        url = "/profile/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["size"], 1)
        self.assertEqual(len(json_response["lineitems"]), 1)

        #Return json_response for use in the lineitems test
        return json_response


    def test_remove_product_from_order(self):
        """
        Ensure we can remove a product from an order.
        """
        # Add product
        self.test_add_product_to_order()

        # Remove product from cart
        url = "/lineitems/1"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was removed
        url = "/profile/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["size"], 0)
        self.assertEqual(len(json_response["lineitems"]), 0)

    def test_complete_order_by_adding_payment_type(self):

        # Add product to order"
        self.test_add_product_to_order()

        #Add payment method to profile:
        url="/paymenttypes"
        data = {'merchant_name':"American Depress",
                'account_number':123456,
                'expiration_date':"2026-01-15",
                "create_date": datetime.date.today()} 
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        # Verify payment was added
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Add payment type do order
        url = "/orders/1"
        data = {
        "payment_type": 1
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(url, data, format='json')
        
        # Verify the order was completed successfully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify payment type was added
        url = "/orders/1"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        #Take the payment_type url and slash/split the URL to get the id
        payment_type_url = json_response["payment_type"]
        payment_type_id = int(payment_type_url.rstrip('/').split('/')[-1])
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payment_type_id, 1)
        
        #Return the response to be accessed by the lineitem function below
        return json_response
    
    def test_new_line_item_added_to_new_order(self):
        """
        Ensure that when a new product is added after a completed order, it is added to the new order and not the completed order.
        """
        #Add a closed order
        closed_order_response = self.test_complete_order_by_adding_payment_type()
        closed_order_id = closed_order_response.get("id")
        #Add product to the cart (copied directly from test_add_product_to_order)
        product_added_response = self.test_add_product_to_order()
        order_url = product_added_response["url"]
        order_id = int(order_url.rstrip('/').split('/')[-1])

        #Verify that the returned order is open and not closed
        self.assertNotEqual(
            order_id,
            closed_order_id,
            "A new line items should be added to an open order, not an order that is closed."
        )

        #Verify that the order has the correct number of lineitems and size should be 1
        self.assertEqual(product_added_response["size"],1)
        self.assertEqual(len(product_added_response["lineitems"]), 1)

import datetime
import json
from rest_framework import status
from rest_framework.test import APITestCase


class PaymentTests(APITestCase):
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


    def test_create_payment_type(self):
        """
        Ensure we can add a payment type for a customer.
        """
        # Add product to order
        url = "/paymenttypes"
        data = {
            "merchant_name": "American Express",
            "account_number": "111-1111-1111",
            "expiration_date": "2024-12-31",
            "create_date": datetime.date.today()
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["merchant_name"], "American Express")
        self.assertEqual(json_response["account_number"], "111-1111-1111")
        self.assertEqual(json_response["expiration_date"], "2024-12-31")
        self.assertEqual(json_response["create_date"], str(datetime.date.today()))

    def test_delete_payment_type(self):
        """
        Ensure we can remove a paymenttype from an order.
        """
    


        url = "/paymenttypes"
        creation_data = {
            "merchant_name": "American Express",
            "account_number": "111-1111-1111",
            "expiration_date": "2024-12-31",
            "create_date": datetime.date.today()
    }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url, creation_data, format='json')
        json_response = json.loads(response.content)

        paymenttype_id = json_response["id"]

        url = "/paymenttypes"
        data = {"paymenttype_id": paymenttype_id}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = "/paymenttypes"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.assertEqual(json_response["merchant_name"], 0)
        self.assertEqual(json_response["account_number"], 0)
        self.assertEqual(json_response["expiration_date"], 0)
        self.assertEqual(json_response["create_date"], 0)
        # self.assertEqual(json_response["deleted"], 0)
        # self.assertEqual(json_response["deleted_by_cascade"], 0)
        # self.assertEqual(json_response["customer_id"], 0)



        

        
        
# def test_delete_payment_type(self):
#     """
#     Ensure we can delete a payment type.
#     """
#     # First create a payment type
#     url = "/paymenttypes"
#     data = {
#         "merchant_name": "American Express",
#         "account_number": "111-1111-1111",
#         "expiration_date": "2024-12-31",
#         "create_date": datetime.date.today()
#     }
#     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
#     response = self.client.post(url, data, format='json')
#     json_response = json.loads(response.content)
    
#     # Get the ID of the created payment type
#     payment_type_id = json_response["id"]
    
#     # Delete the specific payment type
#     url = f"/paymenttypes/{payment_type_id}"
#     response = self.client.delete(url)
    
#     # Check that the deletion was successful
#     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
#     # Verify the payment type is gone by trying to get it
#     response = self.client.get(url)
#     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
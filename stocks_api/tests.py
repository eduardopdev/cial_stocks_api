from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class StockAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('stocks')
        self.stock = "AAPL"
        self.url_post = reverse('stocks_post', args=[self.stock])
        self.url_post_invalid = reverse('stocks_post', args=['Eduardo'])

    def test_get_valid_stock(self):
        """
        Testa a resposta da api para GET request de um stock ticker valido
        """
        response = self.client.get(self.url+f"?ticker={self.stock}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_invalid_stock(self):
        """
        Testa a resposta da api para GET request de um stock ticker invalido
        """
        response = self.client.get(self.url, args=['EDUARDO'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_valid_stock(self):
        """
        Testa a post request para uma stock válida
        """
        data = {
            "amount" : 4
        }
        response = self.client.post(self.url_post, data, format='json')  # Sending the POST request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Check for 201 status
    
    def test_post_invalid_stock(self):
        """
        Testa a post request para uma stock válida
        """
        data = {
            "amount" : 4
        }
        response = self.client.post(self.url_post_invalid, data, format='json')  # Sending the POST request
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Check for 201 status
    
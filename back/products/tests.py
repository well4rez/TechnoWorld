from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProdViewsTests(TestCase):
    def test_prod_when_opned(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_search_work(self):
        Product.objects.create(name='Samsung A15', slug='samsung-s24', price=15999.00)
        Product.objects.create(name='test1', slug='test1', price=0.00)
        Product.objects.create(name='test2', slug='test2', price=0.00)

# Create your tests here.

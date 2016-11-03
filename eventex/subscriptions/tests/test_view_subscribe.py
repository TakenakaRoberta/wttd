from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm

#m2a15 6:00
class SubscribeGet(TestCase):

    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)
        
    def test_template(self):
        """Must return /subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contains input tags"""
        tags = (
            ('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_crsf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)
        

class SubscribePostValid(TestCase):

    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='12345678901', email='henrique@bastos.net', phone='987654321')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


class SubscribePostInvalid(TestCase):    
    def setUp(self):    
        self.resp = self.client.post('/inscricao/', {})
    
    def test_post(self):
        """Invalid POST should not redirect"""    
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):    
        """template ..."""    
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):    
    def test_message(self):    
        #m2a13 37:21    
        data = dict(name='Henrique Bastos', cpf='12345678901', email='henrique@bastos.net', phone='1')    
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso')
    

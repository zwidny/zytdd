# -*- coding: utf-8 -*-
import requests
from accounts.models import ListUser


class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        # send the assertion to mozilla's verifier service.
        data = {
            'assertion': assertion,
            'audience': 'localhost'
        }
        resp = requests.get('https://verifier.login.persona.org/verify',
                            data=data)
        if resp.ok:
            verification_data = resp.json()
            if verification_data['status'] == 'okay':
                email = verification_data['email']
                try:
                    return self.get_user(email)
                except ListUser.DoesNotExist:
                    return ListUser.objects.create(email=email)

    def get_user(self, email):
        return ListUser.objects.get(email=email)

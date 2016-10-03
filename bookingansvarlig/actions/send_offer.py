from django.core.mail import EmailMessage, EmailMultiAlternatives


__author__ = 'Weronika'


def send_offer(address):
    # norwegian signs do not work
    email = EmailMessage('hyttatur', 'Skal vi gaa paa hytta? Wera', to=['weronika@stud.ntnu.no','weronika.ada@gmail.com'])
    email.send(fail_silently=False)
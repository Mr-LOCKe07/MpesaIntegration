from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from .credentials import MpesaAccessToken, LipanaMpesaPpassword

from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'home.html', {'navbar': 'home'})


def token(request):
    consumer_key = 'fuJOu6FXqel8A9caNGWjdZNSnzNVG9WGea4kam41oa1GwlHg'
    consumer_secret = 'TJCGQwaZ1EA0S7EJUtatp5r3eVl0jTafyBOJnc6fTCcpqDlGUjN3rqrYCzIWePH8'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def pay(request):
    global api_url, headers
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/mpesa_app/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Blaise Eugene",
            "TransactionDesc": "Web Development Charges"
        }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse("success")


def stk(request):
    return render(request, 'pay.html', {'navbar': 'stk'})
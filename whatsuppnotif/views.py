from twilio.rest import Client
from medtech.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from firebase_admin.messaging import Message, AndroidNotification, AndroidConfig, Notification
from fcm_django.models import FCMDevice
from rest_framework.response import Response

order_details = {
    'date_of_visit': '03/04/2021',
    'address': 'No 1, Ciroma Chukwuma Adekunle Street, Ikeja, Lagos'
}


def send_notification(request):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    if request.method == 'POST':
        user_whatsapp_number = request.POST['user_number']

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='You should visit your doctor on {}. Address details: {}'.format(
                order_details['date_of_visit'],
                order_details['address']),
            to='whatsapp:+{}'.format(user_whatsapp_number)
        )

        return HttpResponse('Great! Expect a message...')

    return render(request, 'phone.html')


class PushApi(APIView):
    def post(self, request):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        user_whatsapp_number = request.data['user_number']
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='You should visit your doctor on {}. Address details: {}'.format(
                order_details['date_of_visit'],
                order_details['address']),
            to='whatsapp:+{}'.format(user_whatsapp_number)
        )
        return Response("Success?")


#Notification for app


class FCMTest(APIView):
    def post(self, request):

        reg_id = request.data['reg_ids']
        FCMDevice.objects.create(registration_id=reg_id, type="android")

        return Response("Success?")

    def get(self, request):
        message = Message(
            android=AndroidConfig(notification=AndroidNotification(title="название", body="text", sound="default"), )
        )
        reg_id = FCMDevice.objects.get()
        FCMDevice.objects.filter(registration_id=reg_id).send_message(message)

        return Response("Success?")
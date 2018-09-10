from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_twilio.decorators import twilio_view

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import random

from .models import Entry

@twilio_view
@csrf_exempt
def sms_response(request):
    # Define entry
    entry = Entry()
    entry.name = request.POST.get('Body', '')
    entry.number = request.POST.get('From', '')
    entry.save()

    # Start our TwiML response
    resp = MessagingResponse()

    # Add a text message
    msg = "%s, thank you for entering the giveaway for \"Feature Engineering for Machine Learning\" by our speaker, Amanda Casari. Check out that sweet owl!" % (entry.name)
    msg = resp.message(msg)

    # Add a picture message
    msg.media("https://covers.oreillystatic.com/images/0636920049081/lrg.jpg")

    return HttpResponse(str(resp))

@csrf_exempt
def select_and_notify(request):
    # Define client: Replace strings with actual account SID & auth token
    client = Client('account_sid', 'auth_token')
    # I also tried the following command to pull messages directly from Twilio
    # messages = client.messages.list()
    # But it ended up being more effective in the moment to start by pulling entire objects
    # and then making an array of contest entrant names.
    # (At the very least, I wanted to be able to randomize the selection of our winner!)
    items = Entry.objects.all()
    Entries = []
    for message in items:
        name = message.name
        Entries.append(name)

    winner = random.choice(Entries)

    for entry in items:
        number = entry.number
        if entry.name == winner:
            msg = "%s, you won! Have fun digging into Feature Engineering! If you are not present (thank you for watching the live stream!), we will reach out to you ASAP to coordinate. In the meantime, you can peek at the GitHub repo here: https://github.com/alicezheng/feature-engineering-book" % entry.name
        else:
            msg = "Thank you for learning with us, %s. You didn't win this evening, but you can get a copy for yourself at http://shop.oreilly.com/product/0636920049081.do and the GitHub repo is available to everyone at https://github.com/alicezheng/feature-engineering-book" % entry.name
        message = client.messages.create(
            body = msg,
            # Replace the following zeros with your project's twilio number
            from_='+00000000000',
            to=number,
        )
        print(message.sid)

    return HttpResponse(str(Entries) + "The winner is " + str(winner))

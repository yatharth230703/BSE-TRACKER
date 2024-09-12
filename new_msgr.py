from twilio.rest import Client
def whtsapp(msg):
  
  account_sid = 'AC599f47483826015f1f06f5e4c9219b78'
  auth_token = '7ea1bf3de7c160a8ada786dd58f0e484'
  client = Client(account_sid, auth_token)
  message1 = client.messages.create(
  from_='whatsapp:+14155238886',
  body=msg,
  to='whatsapp:+96566089042'
  )
  return "message sent" + message1.sid
whtsapp(f"Welcome User :")
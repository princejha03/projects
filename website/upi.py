import random
from twilio.rest import Client

value= random.randint(10000,100000)
print("The opt is")
print(value)
account_sid = 'ACedeb4fff9d76462c3c38216934254077'
auth_token = '76379d5f2feba58684ec6467546c27ce'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+13525030445',
  body= value,
  to='+918826181378'
)


from urllib import response
import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes":74, "name":"Joe Mama", "views":32999},
        {"likes":1999, "name":"Uzair makes a REST API", "views":8999},
        {"likes":35, "name":"Hello mfer", "views":2000}]
    
for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())
# this is going to send a get request to 
# "http://127.0.0.1:5000/helloworld"
# When you write a ".post" instead it won't work because
# we (at this time of writing notes) did not have a "post" method

# this will print the response in json format and not in the actual
# response format
# print(response.json())
input()

response = requests.delete(BASE + "video/0")
print(response)

input()

response = requests.get(BASE + "video/2")
print(response.json())
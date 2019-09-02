import requests

apibasepoint = "http://localhost:5000"

r = requests.put(f"{apibasepoint}/user/new", json = {
    "name": "Developer Test 1",
    "description": "I'm just a lonely dev",
    "email": "dev@example.org",
    "password": "password"
})
result = r.json()
print(result)
#newuserid = result["id"]
newuserid = 9999999999

r = requests.get(f"{apibasepoint}/user/{newuserid}/getverifytoken")
result = r.json()
print(result)

r = requests.get(f"{apibasepoint}/user/{newuserid}/verify?token={result['verifytoken']}")
result = r.json()
print(result)

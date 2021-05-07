import requests
id = "c96c142f"
resultado_api_user = requests.get(f"http://localhost:5001/listar_user/{id}/").json()
if len(resultado_api_user) == 1:
    print(resultado_api_user[0]["nome"])

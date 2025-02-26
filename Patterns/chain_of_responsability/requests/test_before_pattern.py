import requests


def test_api_without_pattern():
    # Realizar la petición a la API
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")

    # Validar código de estado
    if response.status_code != 200:
        print(f"❌ Invalid status code: {response.status_code}")
        print("❌ API Test Failed")
        return
    print("✅ Status code is valid")

    # Validar que la respuesta sea JSON válido
    try:
        data = response.json()
        print("✅ Response is valid JSON")
    except ValueError:
        print("❌ Response is not valid JSON")
        print("❌ API Test Failed")
        return

    # Validar campos requeridos
    required_fields = ["id", "name", "email"]
    for field in required_fields:
        if field not in data:
            print(f"❌ Missing field: {field}")
            print("❌ API Test Failed")
            return
    print("✅ All required fields are present")

    # Si todas las validaciones pasan, la prueba es exitosa
    print("🎉 API Test Passed:", data)


# Ejecutar prueba
test_api_without_pattern()
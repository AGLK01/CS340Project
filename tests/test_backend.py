import requests

# Base URL of your Flask application
BASE_URL = "http://127.0.0.1:5000"

# Test fetching all employees
def test_get_employees():
    url = "http://127.0.0.1:5000/employees"
    response = requests.get(url)
    print("Raw Response Content:", response.text)  # Add this line
    if response.status_code == 200:
        print("GET /employees - Success:", response.json())
    else:
        print("GET /employees - Failed:", response.json())

# Test adding a new employee
def test_add_employee():
    new_employee = {
        "EID": 11,
        "name": "John Doe",
        "access_level": "medium",
        "IsManager": False,
        "IsMP": True
    }


    response = requests.post(f"{BASE_URL}/add_employee", json=new_employee)
    if response.status_code == 200:
        print("POST /add_employee - Success!")
        print(response.json())
    else:
        print("POST /add_employee - Failed:", response.json())

# Run tests
if __name__ == "__main__":
    print("Running API Tests...")
    test_get_employees()
    test_add_employee()
    test_get_employees()
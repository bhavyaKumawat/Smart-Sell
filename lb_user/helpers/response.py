def get_response_template():
    return {
        "employee": {
            "EmployeeId": "",
            "EmployeeName": "",
            "Rest_Number": "",
            "SmartSellAmount": 0.0,
            "SuccessSmartSellCount": 0,
            "TotalSmartSellCount": 0,
            "Percentage": 0.0,
            "rank": {
                "restaurant": 0,
                "network": 0
            }
        },
        "store": {
            "LocationId": "",
            "Rest_Number": "",
            "SmartSellAmount": 0.0,
            "SuccessSmartSellCount": 0,
            "TotalSmartSellCount": 0,
            "Percentage": 0.0,
            "rank": {
                "network": 0
            }
        },
        "top_emp_in_store": [],
        "top_emp_in_network": [],
        "top_store_in_network": []
    }

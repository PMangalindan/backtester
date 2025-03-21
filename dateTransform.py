from datetime import datetime, timedelta

def next_sunday(date_str):
    # Parse input date
    date_obj = datetime.strptime(date_str, "%Y.%m.%d")

    # Calculate days until the next Sunday (0=Monday, ..., 6=Sunday)
    days_until_sunday = (6 - date_obj.weekday()) % 7
    days_until_sunday = 7 if days_until_sunday == 0 else days_until_sunday  # Ensure it moves to next Sunday

    # Get the next Sunday
    next_sunday_date = date_obj + timedelta(days=days_until_sunday)

    # Return in the same format
    return next_sunday_date.strftime("%Y.%m.%d")

# Example usage
# print(next_sunday("2024.07.15"))  # Correct output: "2025.03.23"
# print(next_sunday("2024.03.14"))  # Correct output: "2024.03.17"
# print(next_sunday("2025.03.16"))  # Correct output: "2025.03.23"



def next_saturday(date_str):
    # Parse input date
    date_obj = datetime.strptime(date_str, "%Y.%m.%d")

    # Calculate days until the next Saturday (5 = Saturday)
    days_until_saturday = (5 - date_obj.weekday()) % 7
    days_until_saturday = 7 if days_until_saturday == 0 else days_until_saturday  # Ensure it moves to next Saturday

    # Get the next Saturday
    next_saturday_date = date_obj + timedelta(days=days_until_saturday)

    # Return in the same format
    return next_saturday_date.strftime("%Y.%m.%d")

# Example usage
# print(next_saturday("2025.03.17"))  # Output: "2025.03.22"
# print(next_saturday("2024.03.14"))  # Output: "2024.03.16"
# print(next_saturday("2025.03.15"))  # Output: "2025.03.22"



def next_friday(date_str):
    # Parse input date
    date_obj = datetime.strptime(date_str, "%Y.%m.%d")

    # Calculate days until the next Friday (4 = Friday)
    days_until_friday = (4 - date_obj.weekday()) % 7
    days_until_friday = 7 if days_until_friday == 0 else days_until_friday  # Ensure it moves to next Friday

    # Get the next Friday
    next_friday_date = date_obj + timedelta(days=days_until_friday)

    # Return in the same format
    return next_friday_date.strftime("%Y.%m.%d")

# Example usage
# print(next_friday("2025.03.17"))  # Output: "2025.03.21"
# print(next_friday("2024.03.14"))  # Output: "2024.03.15"
# print(next_friday("2025.03.14"))  # Output: "2025.03.21"



print(next_sunday("2025.03.29"))
print(next_friday(next_sunday("2025.03.29")))
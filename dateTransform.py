from datetime import datetime, timedelta

def add_days_to_date(date_str, days_to_add):
    """
    Adds a given number of days to a date string in 'YYYY.MM.DD' format.

    :param date_str: The input date string (e.g., "2024.08.14")
    :param days_to_add: The number of days to add
    :return: The new date string in 'YYYY.MM.DD' format
    """
    date_obj = datetime.strptime(date_str, "%Y.%m.%d")
    new_date = date_obj + timedelta(days=days_to_add)
    return new_date.strftime("%Y.%m.%d")

# Example usage
new_date = add_days_to_date("2024.03.14", 5)
print(new_date)  # Output: "2024.08.19"

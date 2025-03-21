import sys
from datetime import datetime

def check_expiry(expiry_date: str):
    """
    Exits the program if the current date is past the specified expiry date.
    
    :param expiry_date: The expiry date in "YYYY-MM-DD" format.
    """
    current_date = datetime.now().date()
    expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()

    if current_date > expiry_date:
        print(f"Program expired! Current date {current_date} is past {expiry_date}. Exiting...")
        sys.exit(1)

# Example usage
check_expiry("2025-03-20")
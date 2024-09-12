from datetime import datetime, timedelta, time

def is_time_in_range_ist(start_time_str, end_time_str):
    """
    Check if the current IST time lies between the given start and end times.

    Args:
        start_time_str (str): Start time in HH:MM format.
        end_time_str (str): End time in HH:MM format.

    Returns:
        bool: True if the current IST time is within the range, False otherwise.
    """
    # Convert string times to time objects
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()
    
    # Get the current UTC time and convert to IST
    now_utc = datetime.utcnow()
    now_ist = now_utc + timedelta(hours=5, minutes=30)
    current_time_ist = now_ist.time()

    # Check if current time is within the range
    if start_time <= end_time:
        return start_time <= current_time_ist <= end_time
    else:
        # Over midnight case (e.g., 23:00 to 02:00)
        return current_time_ist >= start_time or current_time_ist <= end_time

# Example usage
#start_time = "13:40"  # 10:00 PM IST
#end_time = "13:50"    # 2:00 AM IST
#if is_time_in_range_ist(start_time, end_time):
#    print("Current time is within the range.")
#else:
#    print("Current time is not within the range.")


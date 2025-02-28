def convert_time(days, hours, minutes, seconds):
    """
    function converts time from #d, #h, #m, #s format to HH:MM:SS format.
    """

    total_hours = (days * 24) + hours
    return f"{total_hours:02d}:{minutes:02d}:{seconds:02d}"


# use collected data to convert time
days = 4
hours = 19
minutes = 54
seconds = 42

converted_values = convert_time(days, hours, minutes, seconds)
print(converted_values)


#DATE AND TIME  VALIDATION  (Gabriel)

def is_valid_date(text):
    parts = text.split("-")
    if len(parts) != 3:
        return False
    year_part = parts[0]
    month_part = parts[1]
    day_part = parts[2]
    if not year_part.isdigit() or not month_part.isdigit() or not day_part.isdigit():
        return False
    if len(year_part) != 4:
        return False
    if int(month_part) < 1 or int(month_part) > 12:
        return False
    if int(day_part) < 1 or int(day_part) > 31:
        return False
    return True


def format_time(text):
    cleaned = text.strip().lower()
    if cleaned in ["all", "all day", "allday", "all-day", ""]:
        return "ALL DAY"
    parts = cleaned.split(":")
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        return "%02d:%02d" % (int(parts[0]), int(parts[1]))
    return text


def is_valid_time(text):
    cleaned = text.strip().lower()
    if cleaned in ["all", "all day", "allday", "all-day", ""]:
        return True
    parts = cleaned.split(":")
    if len(parts) != 2:
        return False
    hour_part = parts[0]
    minute_part = parts[1]
    if not hour_part.isdigit() or not minute_part.isdigit():
        return False
    if int(hour_part) < 0 or int(hour_part) > 23:
        return False
    if int(minute_part) < 0 or int(minute_part) > 59:
        return False
    return True


def get_event_status(saved_status, event_date, today):
    if saved_status == "done":
        return "done"
    if event_date < today:
        return "due"
    if event_date == today:
        return "ongoing"
    return "pending"

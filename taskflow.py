# MODULE 5: CALENDAR DISPLAY & TABLE RENDERER (Rita)
# ==============================================================================

def show_event_list():
    raw_events = db.get_user_events(CURRENT_USER)
    if len(raw_events) == 0:
        print(f"  No events yet for {CURRENT_USER}.")
        return

    today = str(date.today())
    print("  -------------------------------------------------------------------------")
    print("  ID | Title | Date | Time | Category | Status | Owner")
    print("  -------------------------------------------------------------------------")
    for row in raw_events:
        ev = Event.from_row(row)
        formatted_time = format_time(ev.event_time)
        current_status = get_event_status(ev.status, ev.event_date, today).upper()
        print(f"  #{ev.id} | {ev.title} | {ev.event_date} {formatted_time} | {ev.category_name} | {current_status} | Owner: {ev.owner_name}")
        if ev.details:
            print(f"      details: {ev.details}")
    print("  -------------------------------------------------------------------------")


def show_calendar():
    today = date.today()
    month_title = f"{calendar.month_name[today.month]} {today.year}"
    print("  +-----------------------------------+")
    print(f"  |  {month_title.center(31)}  |")
    print("  +-----------------------------------+")
    print("  |   Mo  Tu  We  Th  Fr  Sa  Su      |")
    print("  |  -------------------------------  |")

    for week in calendar.monthcalendar(today.year, today.month):
        line = "  |  "
        for day in week:
            if day == 0:
                cell = "    "
            elif day == today.day:
                cell = f" [{day}]" if day < 10 else f"[{day}]"
            else:
                cell = f"   {day}" if day < 10 else f"  {day}"
            line += cell
        line = line.ljust(37) + "|"
        print(line)

    print("  +-----------------------------------+")


def view_all():
    print("")
    show_calendar()
    print("")
    show_event_list()
    print("")


def view_member_calendar():
    print("")
    owners = db.get_all_owners()
    if len(owners) == 0:
        print("  No members have added events yet.")
        return

    print("  -----------------------------")
    print("  Users with Calendars:")
    print("  -----------------------------")
    number = 1
    for owner_name in owners:
        print(f"   {number}) {owner_name}")
        number += 1
    print("  -----------------------------")
    print("")

    choice = input("  Pick a user number (or Enter for all): ").strip()
    if choice == "":
        view_all()
        return

    if choice.isdigit() and 1 <= int(choice) <= len(owners):
        member_name = owners[int(choice) - 1]
    else:
        member_name = choice

    raw_events = db.get_events_by_owner(member_name)
    if len(raw_events) == 0:
        print(f"  No events found for owner '{member_name}'.")
        return

    today = date.today()
    month_title = f"{calendar.month_name[today.month]} {today.year} - {member_name.capitalize()}"
    print("  +-----------------------------------+")
    print(f"  |  {month_title.center(31)}  |")
    print("  +-----------------------------------+")
    print("  |   Mo  Tu  We  Th  Fr  Sa  Su      |")
    print("  |  -------------------------------  |")

    for week in calendar.monthcalendar(today.year, today.month):
        line = "  |  "
        for day in week:
            if day == 0:
                cell = "    "
            elif day == today.day:
                cell = f" [{day}]" if day < 10 else f"[{day}]"
            else:
                cell = f"   {day}" if day < 10 else f"  {day}"
            line += cell
        line = line.ljust(37) + "|"
        print(line)

    print("  +-----------------------------------+")
    print("")

    today_str = str(date.today())
    print("  -------------------------------------------------------------------------")
    print("  ID | Title | Date | Time | Category | Status | Owner")
    print("  -------------------------------------------------------------------------")
    for row in raw_events:
        ev = Event.from_row(row)
        formatted_time = format_time(ev.event_time)
        current_status = get_event_status(ev.status, ev.event_date, today_str).upper()
        print(f"  #{ev.id} | {ev.title} | {ev.event_date} {formatted_time} | {ev.category_name} | {current_status} | Owner: {ev.owner_name}")
        if ev.details:
            print(f"      details: {ev.details}")
    print("  -------------------------------------------------------------------------")
    print("")

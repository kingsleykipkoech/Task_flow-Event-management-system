import sys
import os
import calendar
import smtplib
import threading
import time
from datetime import date, datetime, timedelta
import connection as db

# USER IDENTITY and ABILITY

CURRENT_USER = "Planner"


def select_user_identity():
    global CURRENT_USER
    while True:
        all_members = db.get_all_members()
        print("")
        print("             Who are you?              ")
        print("  ---------------------------------------")
        number = 1
        for member in all_members:
            print(f"   {number}) {member[1]}")
            number += 1
        print(f"   {number}) + Edit / Manage Users")
        print("  -----------------------------")
        print("")
        choice = input("  Pick your name number: ").strip()
        while not choice.isdigit() or int(choice) < 1 or int(choice) > len(all_members) + 1:
            choice = input("  Invalid selection. Pick your name number: ").strip()

        if int(choice) == len(all_members) + 1:
            print("")
            print("  -----------------------------")
            print("  Edit / Manage Users Options:")
            print("  -----------------------------")
            print("   1) Add a new user")
            print("   2) Delete an existing user")
            print("  -----------------------------")
            sub_choice = input("  Pick 1 or 2: ").strip()

            if sub_choice == "1":
                new_name = input("  Enter new user name: ").strip()
                if new_name != "":
                    db.add_member(new_name)
                    CURRENT_USER = new_name
                    print(f"\n  Logged in as: {CURRENT_USER}")
                    break
                else:
                    CURRENT_USER = "Planner"
                    print(f"\n  Logged in as: {CURRENT_USER}")
                    break
            elif sub_choice == "2":
                if len(all_members) == 0:
                    print("  No users available to delete.")
                    continue
                print("")
                print("  Pick user number to delete:")
                del_num = 1
                for member in all_members:
                    print(f"   {del_num}) {member[1]}")
                    del_num += 1
                del_choice = input("  User number to delete: ").strip()
                if del_choice.isdigit() and 1 <= int(del_choice) <= len(all_members):
                    target_name = all_members[int(del_choice) - 1][1]
                    db.delete_member(target_name)
                    print(f"  User '{target_name}' deleted successfully.")
                else:
                    print("  Invalid selection.")
                continue
            else:
                print("  Invalid choice.")
                continue
        else:
            CURRENT_USER = all_members[int(choice) - 1][1]
            print(f"\n  Logged in as: {CURRENT_USER}")
            break


def pick_role():
    print("")
    print("       Welcome to TaskFlow Planner       ")
    print("  ---------------------------------------")
    print("")
    print("  Choose your role:")
    print("  " + "-" * 41)
    print("  1) Planner  -  full access")
    print("  2) Viewer   -  view and search only")
    print("  " + "-" * 41)
    print("")
    choice = input("  Enter 1 or 2: ").strip()
    while choice != "1" and choice != "2":
        choice = input("  Please enter 1 or 2: ").strip()
    if choice == "1":
        print("")
        print("  Logged in as Planner.")
        return "planner"
    else:
        print("")
        print("  Logged in as Viewer.")
        return "viewer"

# EVENT CREATION & CATEGORIES 

class Event:
    def __init__(self, event_id, title, event_date, event_time, details, status, category_name, owner_name="Planner"):
        self.id = event_id
        self.title = title
        self.event_date = event_date
        self.event_time = event_time
        self.details = details
        self.status = status
        self.category_name = category_name
        self.owner_name = owner_name

    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        owner_name = row[7] if len(row) > 7 and row[7] else "Planner"
        return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], owner_name)


def choose_category():
    all_categories = db.get_all_categories()
    print("")
    print("  Categories:")
    print("  -----------------------------")
    number = 1
    for category in all_categories:
        category_name = category[1]
        print(f"   {number}) {category_name}")
        number = number + 1
    print("  -----------------------------")
    print("")
    choice = input("  Pick a category number: ").strip()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(all_categories):
        choice = input("  Invalid. Pick a category number: ").strip()
    chosen_category = all_categories[int(choice) - 1]
    return chosen_category[0]


def add_event():
    print("")
    print("            Add New Event            ")
    print("  ---------------------------------------")
    print("")
    title = input("  Event title (or Enter to cancel): ").strip()
    if title == "" or title.lower() == "cancel":
        print("  Event creation cancelled.")
        return
    date_input = input("  Date (YYYY-MM-DD): ").strip()
    while not is_valid_date(date_input):
        date_input = input("  Invalid. Date (YYYY-MM-DD): ").strip()
    time_input = input("  Time (HH:MM or leave empty for All Day): ").strip()
    while not is_valid_time(time_input):
        time_input = input("  Invalid. Time (HH:MM or you can leave empty for All Day): ").strip()
    time_input = format_time(time_input)
    details = input("  Details (optional): ").strip()
    category_id = choose_category()

    new_event_id = db.add_event(title, date_input, time_input, details, category_id, CURRENT_USER)
    print("")
    print("  Event added successfully!")
    print("")
    emails_input = input("  Add a person/people to remind you (comma or space separated): ").strip()
    if emails_input != "":
        emails_input = emails_input.replace(",", " ")
        for one_email in emails_input.split():
            one_email = one_email.strip()
            if one_email != "":
                db.add_attendee(new_event_id, one_email)
        print("  Emails added.")


def manage_categories():
    print("")
    all_categories = db.get_all_categories()
    print("  Current Categories:")
    print("  -----------------------------")
    for category in all_categories:
        print(f"   - {category[1]}")
    print("  -----------------------------")
    print("")
    name = input("  Enter new category name (or Enter to go back): ").strip()
    if name == "":
        return
    db.add_category(name)
    print(f"  Category '{name}' added!")


# DATE  AND TIME VALIDATION 
def is_valid_date(text):
    parts = text.split("-")
    if len(parts) != 3:
        return False
    year_part, month_part, day_part = parts[0], parts[1], parts[2]
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
    hour_part, minute_part = parts[0], parts[1]
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
#  CALENDAR DISPLAY 
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


=============================================================================
# MODULE 3: EVENT CREATION & CATEGORY MANAGEMENT (VANESSA)
# ==============================================================================

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

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
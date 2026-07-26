# SEARCH,EDIT, DELETE & ICS IMPORTS (Kingsley)

def search_events():
    print("")
    keyword = input("  Search keyword: ").strip().lower()
    raw_results = db.search_events(keyword)
    if len(raw_results) == 0:
        print("  No matching events.")
        return

    today = str(date.today())
    print("")
    print("  Search results:")
    print("  -------------------------------------------------------------------------")
    for row in raw_results:
        ev = Event.from_row(row)
        formatted_time = format_time(ev.event_time)
        current_status = get_event_status(ev.status, ev.event_date, today).upper()
        print(f"  #{ev.id} | {ev.title} | {ev.event_date} {formatted_time} | {ev.category_name} | {current_status} | Owner: {ev.owner_name}")
    print("  -------------------------------------------------------------------------")
    print("")



def edit_event():
    print("")
    show_event_list()
    print("")
    event_id = input("  Enter event id to edit: ").strip()
    if not event_id.isdigit():
        print("  Invalid id.")
        return
    title = db.get_event_title(event_id)
    if title is None:
        print("  No event with that id.")
        return

    print("")
    print(f"  Editing: {title}")
    print("  -----------------------------------")
    print("  1) Mark as done")
    print("  2) Add participants (people to remind you)")
    print("  -----------------------------------")
    choice = input("  Pick 1 or 2: ").strip()

    if choice == "1":
        db.mark_event_done(event_id)
        print("  Marked done.")
    elif choice == "2":
        emails_input = input("  Enter participant emails (comma or space separated): ").strip()
        if emails_input == "":
            print("  No emails entered.")
            return
        emails_input = emails_input.replace(",", " ")
        for one_email in emails_input.split():
            one_email = one_email.strip()
            if one_email != "":
                db.add_attendee(event_id, one_email)
        print(f"  Participants added to: {title}")
    else:
        print("  Nothing changed.")


def delete_event():
    print("")
    show_event_list()
    print("")
    event_id = input("  Enter event id to delete: ").strip()
    if not event_id.isdigit():
        print("  Invalid id.")
        return
    deleted_count = db.delete_event(event_id)
    if deleted_count == 0:
        print("  No event with that id.")
    else:
        print("  Deleted.")

def import_ics():
    print("")
    source = input("  Enter .ics file path: ").strip()
    if source == "":
        return

    if not os.path.exists(source):
        print("  File not found.")
        return
    try:
        with open(source, encoding='utf-8') as ics_file:
            all_lines = ics_file.readlines()
    except Exception:
        print("  Could not read file.")
        return

    imports_category_id = db.get_category_id("Imports")
    title = ""
    event_date = ""
    event_time = "00:00"
    imported_count = 0

    for raw_line in all_lines:
        line = raw_line.strip()

        if line.startswith("SUMMARY:"):
            title = line[8:]

        elif line.startswith("DTSTART"):
            value = line.split(":")[-1]
            date_part = value[0:8]
            if len(date_part) == 8 and date_part.isdigit():
                event_date = date_part[0:4] + "-" + date_part[4:6] + "-" + date_part[6:8]
            if "T" in value:
                time_part = value.split("T")[1]
                if len(time_part) >= 4 and time_part[0:4].isdigit():
                    event_time = time_part[0:2] + ":" + time_part[2:4]

        elif line.startswith("END:VEVENT"):
            if title != "" and event_date != "":
                db.add_event(title, event_date, event_time, "Imported from calendar", imports_category_id, CURRENT_USER)
                imported_count = imported_count + 1
            title = ""
            event_date = ""
            event_time = "00:00"

    print(f"  Imported {imported_count} event(s).")

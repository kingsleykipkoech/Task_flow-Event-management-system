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

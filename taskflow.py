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

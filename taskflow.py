SENDER_EMAIL        = ""
SENDER_APP_PASSWORD = ""


class ReminderService:
    """Handles desktop notifications and email sending for TaskFlow."""
    @staticmethod
    def notify_desktop(title, message):
        if sys.platform != "win32":
            os.system(f'notify-send "{title}" "{message}"')

    @staticmethod
    def send_email(to_email, subject, body):
        load_email_config()
        if not SENDER_EMAIL or not SENDER_APP_PASSWORD:
            return
        try:
            full_message = f"From: {SENDER_EMAIL}\nTo: {to_email}\nSubject: {subject}\n\n{body}"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, full_message)
            server.quit()
        except:
            pass


def load_email_config():
    global SENDER_EMAIL, SENDER_APP_PASSWORD
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".email_config")
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    SENDER_EMAIL = lines[0].strip()
                    SENDER_APP_PASSWORD = lines[1].strip()
        except:
            pass


def configure_email():
    print("")
    print("       Configure Email Reminders        ")
    print("  ---------------------------------------")
    print("")
    email_input = input("  Enter your Gmail address (or Enter to disable): ").strip()
    if email_input == "":
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".email_config")
        if os.path.exists(config_path):
            os.remove(config_path)
        global SENDER_EMAIL, SENDER_APP_PASSWORD
        SENDER_EMAIL = ""
        SENDER_APP_PASSWORD = ""
        print("  Email reminders disabled.")
        return

    password_input = input("  Enter your App Password: ").strip()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".email_config")
    with open(config_path, "w") as f:
        f.write(f"{email_input}\n{password_input}\n")

    load_email_config()
    print("  Email reminders configured successfully!")


def check_email_setup_on_startup():
    load_email_config()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".email_config")
    if SENDER_EMAIL == "" and not os.path.exists(config_path):
        print("")
        print("  +-----------------------------------------+")
        print("  |   First-Time Setup: Email Reminders    |")
        print("  +-----------------------------------------+")
        answer = input("  Would you like to set up email reminders now? (y/n): ").strip().lower()
        if answer == "y" or answer == "yes":
            configure_email()
        else:
            with open(config_path, "w") as f:
                f.write("disabled\n")


def send_email(to_email, subject, body):
    ReminderService.send_email(to_email, subject, body)


def check_upcoming():
    today = str(date.today())
    current_time = datetime.now().strftime("%H:%M")
    events = db.get_events_on_dates(today, today)
    upcoming = []
    for event in events:
        event_date = event[2]
        event_time = format_time(event[3])
        status = event[4]

        if status == "done":
            continue
        if event_time != "ALL DAY" and event_time < current_time:
            continue
        upcoming.append(event)

    if len(upcoming) == 0:
        return

    print("")
    print("  -----------------------------------------")
    print("          Today's Upcoming Events!         ")
    print("  -----------------------------------------")
    for event in upcoming:
        title = event[1]
        event_time = format_time(event[3])
        print(f"   • {title} (TODAY at {event_time})")

        message = f"{title} is happening TODAY at {event_time}"
        ReminderService.notify_desktop("TaskFlow Reminder", message)
    print("  -----------------------------------------")


emailed_events = set()


def email_reminder_loop():
    while True:
        try:
            today = str(date.today())
            now = datetime.now()
            events = db.get_events_on_dates(today, today)
            for event in events:
                event_id = event[0]
                title = event[1]
                raw_time = format_time(event[3])
                status = event[4]
                owner_name = event[5] if len(event) > 5 and event[5] else "Planner"

                if status == "done" or raw_time == "ALL DAY":
                    continue

                try:
                    event_dt = datetime.strptime(today + " " + raw_time, "%Y-%m-%d %H:%M")
                except:
                    continue

                minutes_left = (event_dt - now).total_seconds() / 60

                tag_1hour = str(event_id) + "_1hour"
                tag_30min = str(event_id) + "_30min"

                if 55 <= minutes_left <= 65 and tag_1hour not in emailed_events:
                    attendee_emails = db.get_attendee_emails(event_id)
                    for one_email in attendee_emails:
                        ReminderService.send_email(
                            one_email,
                            f"TaskFlow Reminder: {title} in 1 hour",
                            f"Hi there!\n\nThis is a reminder from TaskFlow.\n\n{owner_name}'s event '{title}' is starting in about 1 hour at {raw_time}.\n\nPlease remind {owner_name} so they don't forget!\n\nBest regards"
                        )
                    emailed_events.add(tag_1hour)

                if 25 <= minutes_left <= 35 and tag_30min not in emailed_events:
                    attendee_emails = db.get_attendee_emails(event_id)
                    for one_email in attendee_emails:
                        ReminderService.send_email(
                            one_email,
                            f"TaskFlow Reminder: {title} in 30 minutes!",
                            f"Hi there!\n\nURGENT reminder from TaskFlow!\n\n{owner_name}'s event '{title}' is starting in about 30 minutes at {raw_time}.\n\nPlease remind {owner_name} NOW!\n\nBest regards"
                        )
                    emailed_events.add(tag_30min)
        except:
            pass
        time.sleep(60)


def send_reminders():
    check_upcoming()


#CLIS entry points
def planner_menu():
    while True:
        print("")
        print("      TaskFlow Planner  [Planner]       ")
        print("  ---------------------------------------")
        print("  1) Add event")
        print("  2) View all events and calendar")
        print("  3) View calendar by user")
        print("  4) Search events")
        print("  5) Edit event")
        print("  6) Delete event")
        print("  7) Import events from .ics file")
        print("  8) Manage categories")
        print("  9) Configure email reminders")
        print("  0) Exit")
        print("  ---------------------------------------")
        print("")
        choice = input("  Choose: ").strip()
        if choice == "1":
            add_event()
        elif choice == "2":
            view_all()
        elif choice == "3":
            view_member_calendar()
        elif choice == "4":
            search_events()
        elif choice == "5":
            edit_event()
        elif choice == "6":
            delete_event()
        elif choice == "7":
            import_ics()
        elif choice == "8":
            manage_categories()
        elif choice == "9":
            configure_email()
        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  Invalid choice.")


def viewer_menu():
    while True:
        print("")
        print("       TaskFlow Planner  [Viewer]       ")
        print("  ---------------------------------------")
        print("  1) View all events and calendar")
        print("  2) View calendar by user")
        print("  3) Search events")
        print("  0) Exit")
        print("  ---------------------------------------")
        print("")
        choice = input("  Choose: ").strip()
        if choice == "1":
            view_all()
        elif choice == "2":
            view_member_calendar()
        elif choice == "3":
            search_events()
        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    db.setup()
    if "--check" in sys.argv:
        send_reminders()
    else:
        check_email_setup_on_startup()
        role = pick_role()
        select_user_identity()
        check_upcoming()
        reminder_thread = threading.Thread(target=email_reminder_loop, daemon=True)
        reminder_thread.start()
        if role == "planner":
            planner_menu()
        else:
            viewer_menu()
import parse_driver
from random import shuffle

def generate_tabling():
    member_commitments = parse_driver.make_parse_get_request('/1/classes/Commitments')['results']
    tabling_slots = get_tabling_slots()
    shuffle(tabling_slots)
    for member_commitment in member_commitments:
        for tabling_slot in tabling_slots:

            member = member_commitment["member_email"]

    print slots

def get_tabling_slots():
    tabling_slots = parse_driver.make_parse_get_request('/1/classes/TestParseTablingSlot')
    return tabling_slots['results']

def init():
    times = [10, 11, 12, 13, 34, 35, 36, 37, 58, 59, 60, 61, 82, 83, 84, 85, 106, 107, 108, 109]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hours = ["10:00am", "11:00am", "12:00pm", "1:00pm"]
    slots = []
    i = 0
    while i != len(times):
        for day in days:
            for hour in hours:
                obj = {
                    "time": times[i],
                    "day": day,
                    "hour": hour,
                    "member_emails": []
                }
                slots.append(obj)
                i += 1
    for slot in slots:
        parse_driver.make_parse_post_request('/1/classes/TestParseTablingSlot', slot)

    # parse_driver_make_parse_post_request('/1/classes/TestParseTablingSlot', {})

if __name__ == "__main__":
    if len(get_tabling_slots()) == 0:
        init()
    else:
        generate_tabling()
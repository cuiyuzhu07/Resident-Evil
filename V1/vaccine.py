"""Vaccine event for V1 (task 3.6).

From VACCINE_DAY on, every day a fraction of the susceptible people is
vaccinated. A vaccination works with probability VACCINE_EFFICACY; an
immune person moves to state 'R' (removed = eliminated or immune).
"""
import random


def make_vaccine_schedule(start_day, rate, last_day):
    """Build the event table {day: fraction of susceptibles to vaccinate}.

    Returns an empty dict when start_day is None (vaccine switched off).
    """
    if start_day is None or rate <= 0:
        return {}
    return {day: rate for day in range(start_day, last_day)}


def vaccinate(people, rate, efficacy):
    """Vaccinate each eligible susceptible person with probability `rate`.

    Eligible means state 'S', not vaccinated before, and not inside a
    shelter. Each vaccinated person becomes immune ('R', person["immune"]
    = True) with probability `efficacy`. Returns how many were vaccinated.
    """
    count = 0
    for person in people:
        if (person["state"] != "S" or person.get("vaccinated")
                or person.get("sheltered")):
            continue
        if random.random() < rate:
            person["vaccinated"] = True
            count += 1
            if random.random() < efficacy:
                person["state"] = "R"
                person["immune"] = True
    return count

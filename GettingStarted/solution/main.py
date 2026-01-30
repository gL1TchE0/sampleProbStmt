import sys
import xml.etree.ElementTree as ET


def parse_input(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    troops = [int(t.find("RateOfDamage").text) for t in root.findall("Troop")]

    ships = {}
    for ship in root.findall("Ship"):
        sid = int(ship.get("id"))
        strength = int(ship.find("Strength").text)
        deadline = int(ship.find("TimeLimit").text)
        ships[sid] = {
            "strength": strength,
            "remaining": strength,
            "deadline": deadline,
            "destroyed": False,
            "time_taken": None
        }

    return troops, ships


def simulate(troops, ships):
    max_rate = max(troops)

    feasible = set()
    impossible = set()

    for sid, s in ships.items():
        if max_rate * s["deadline"] >= s["strength"]:
            feasible.add(sid)
        else:
            impossible.add(sid)

    time = 0
    active = {} 
    max_deadline = max(s["deadline"] for s in ships.values())

    while time < max_deadline:
        time += 1

        for troop in list(active):
            sid = active[troop]
            ship = ships[sid]
            if ship["remaining"] <= 0:
                ship["destroyed"] = True
                ship["time_taken"] = time - 1
                del active[troop]

        free_troops = [i for i in range(len(troops)) if i not in active]

        candidates = [
            sid for sid in feasible
            if not ships[sid]["destroyed"]
            and ships[sid]["remaining"] > 0
            and ships[sid]["deadline"] >= time
        ]

        candidates.sort(key=lambda sid: ships[sid]["deadline"])

        for troop in free_troops:
            if not candidates:
                break
            active[troop] = candidates.pop(0)

        for troop, sid in active.items():
            ships[sid]["remaining"] -= troops[troop]

    destroyed = []
    remaining = []

    for sid, s in ships.items():
        if s["destroyed"]:
            destroyed.append((sid, s["time_taken"]))
        else:
            remaining.append((sid, max(0, s["remaining"])))

    destroyed.sort()
    remaining.sort()
    return destroyed, remaining


def main():
    if len(sys.argv) < 2:
        return

    troops, ships = parse_input(sys.argv[1])
    destroyed, remaining = simulate(troops, ships)

    while True:
        try:
            cmd = input().strip().lower()
        except EOFError:
            break

        if cmd == "exit":
            break
        elif cmd == "print destroyed ships":
            print(f"{len(destroyed)}, {destroyed}")
        elif cmd == "print remaining ships":
            print(f"{len(remaining)}, {remaining}")


if __name__ == "__main__":
    main()

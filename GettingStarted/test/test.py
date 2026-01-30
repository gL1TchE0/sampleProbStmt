import sys
import xml.etree.ElementTree as ET

def main():
    if len(sys.argv) < 2:
        print("Missing input file")
        return

    xml_path = sys.argv[1]
    tree = ET.parse(xml_path)
    root = tree.getroot()  # <Island>

    for troop in root.findall("Troop"):
        name = troop.find("Name").text
        rate = int(troop.find("RateOfDamage").text)
        print(name, rate)

    ship = root.find("Ship")
    ship_id = ship.get("id")
    strength = int(ship.find("Strength").text)
    time_limit = int(ship.find("TimeLimit").text)

    print(ship_id, strength, time_limit)

if __name__ == "__main__":
    main()

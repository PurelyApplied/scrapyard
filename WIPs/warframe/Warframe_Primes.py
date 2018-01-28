import logging
from typing import List

from WIPs.warframe.classes import PrimeComponent, Drop, Rarity, Relic, RelicTier
from WIPs.warframe.data import raw_data


def item_name_formatter(s: str):
    s = s.strip().lower()
    if s.endswith("prime"):
        i_stripped = s.find("prime")
        s = s[:i_stripped].strip()
    return s.title()


def component_name_formatter(s: str):
    s = s.strip().lower()
    words = s.split()
    # if len(words) > 1 and "blueprint" in words[-1].lower():
    #     words.pop(-1)
    return " ".join(words).title()


def build_loot_table(raw_data) -> List[Drop]:
    drop_list = []
    relic_table = {}
    for line in raw_data.split("\n"):
        try:
            item, component, tier, id, rarity, vaulted = line.split(",")

            comp = PrimeComponent(item, component)
            relic = Relic(RelicTier[tier.lower()], id, vaulted.lower() in ("yes", "true"))
            drop = Drop(comp, relic, Rarity[rarity.lower()])

            drop_list.append(drop)
            table_key = repr(relic)
            relic_table[table_key] = relic_table.get(table_key, []) + [drop]
        except ValueError:
            logging.warning("Could not unpack line: '{}'".format(line.strip()))

    return drop_list


# noinspection SpellCheckingInspection
def print_important_drops(tier, *ids):
    PrimeComponent.default_component_formatter = component_name_formatter
    PrimeComponent.default_item_formatter = item_name_formatter

    my_inventory = build_my_inventory()
    possible_drops = get_possible_drops(tier, *ids)
    important_drops = [d for d in possible_drops if d.component not in my_inventory]
    print("{} important drops".format(len(important_drops)))
    for id in ids:
        print("From {} relic:".format(id.upper()))
        print("  " + "\n  ".join([str(d.component) for d in important_drops if d.relic.id == id.upper()]))


def get_possible_drops(tier, *ids):
    relics = [Relic(RelicTier[tier], id) for id in ids]
    all_drops = build_loot_table(raw_data)
    return [d for d in all_drops if d.relic in relics]


# noinspection SpellCheckingInspection
def build_my_inventory():
    my_inventory = []
    for item in ("Akbronco", "Akstiletto", "Braton", "Burston", "Hydroid", "Lex", "Valkyr"):
        my_inventory.append(PrimeComponent(item, "blueprint"))

    my_inventory.append(PrimeComponent("akbroncos", "link"))

    my_inventory.append(PrimeComponent("braton", "barrel"))
    my_inventory.append(PrimeComponent("braton", "receiver"))
    my_inventory.append(PrimeComponent("braton", "stock"))

    my_inventory.append(PrimeComponent("cernos", "upper limb"))
    my_inventory.append(PrimeComponent("cernos", "lower limb"))

    my_inventory.append(PrimeComponent("helios", "systems"))

    my_inventory.append(PrimeComponent("kogaka", "gauntlet"))

    my_inventory.append(PrimeComponent("lex", "barrel"))

    my_inventory.append(PrimeComponent("mirage", "chassis blueprint"))

    my_inventory.append(PrimeComponent("nami skyla", "handle"))

    my_inventory.append(PrimeComponent("paris", "upper limb"))
    my_inventory.append(PrimeComponent("paris", "lower limb"))

    my_inventory.append(PrimeComponent("saryn", "systems blueprint"))

    my_inventory.append(PrimeComponent("tigris", "stock"))

    my_inventory.append(PrimeComponent("valkyr", "neuropics blueprint"))

    return my_inventory

if __name__ == '__main__':
    print_important_drops(
        RelicTier.meso, "g1", "g1", "h1")

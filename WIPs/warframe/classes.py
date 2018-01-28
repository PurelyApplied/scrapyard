from enum import Enum


class Rarity(str, Enum):
    common = "common"
    uncommon = "uncommon"
    rare = "rare"


# noinspection SpellCheckingInspection
class RelicTier(str, Enum):
    lith = "lith"
    meso = "meso"
    axi = "axi"
    neo = "neo"


class Relic:
    def __init__(self, tier: RelicTier, id: str, vaulted=False):
        assert is_char_and_num(id), "Relic ID should be one letter followed by one number"
        self.tier = tier
        self.id = id.upper()
        self.vaulted = vaulted

    def __repr__(self):
        if self.vaulted:
            return "Relic({}, {}, vaulted={})".format(self.tier, self.id, self.vaulted)
        else:
            return "Relic({}, {})".format(self.tier, self.id)

    def __lt__(self, other):
        if tier_to_num(self.tier) != tier_to_num(other.tier):
            return tier_to_num(self.tier) < tier_to_num(other.tier)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return self.tier == other.tier and self.id == other.id


def is_char_and_num(id: str):
    return len(id) == 2 and id[0].isalpha() and id[1].isnumeric()


class PrimeComponent:
    default_item_formatter = None
    default_component_formatter = None

    def __init__(self, item: str, component_name: str, item_formatter=None, component_formatter=None):
        item_formatter = PrimeComponent.default_item_formatter if item_formatter is None else item_formatter
        component_formatter = PrimeComponent.default_component_formatter if component_formatter is None else component_formatter
        item = item.strip()
        self.item = item_formatter(item) if item_formatter is not None else item
        self.component_name = component_formatter(component_name) if component_formatter is not None else component_name

    def __repr__(self):
        return "PrimeComponent({})".format(", ".join(str(x) for x in (self.item, self.component_name)))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __str__(self):
        return "{} -- {}".format(self.item, self.component_name)


class Drop:
    def __init__(self, component, relic, rarity):
        self.component = component
        self.relic = relic
        self.rarity = rarity

    def __repr__(self):
        return "Drop({})".format(", ".join(str(x) for x in (self.component, self.relic, self.rarity)))

    def __hash__(self):
        return hash(repr(self))


def tier_to_num(tier: RelicTier):
    if tier == RelicTier.lith:
        return 1
    if tier == RelicTier.meso:
        return 2
    if tier == RelicTier.axi:
        return 3
    if tier == RelicTier.neo:
        return 4

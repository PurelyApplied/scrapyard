


class Poison:
    _Attributes = ["name",
                   "delivery",
                   "damage",
                   "status",
                   "duration",
                   "delay",
                   "DC",
                   "cost",
                   "other"]

    def __init__(self,
                 name="A default poison", 
                 delivery="injury",
                 damage="1d4",
                 status="none",
                 duration="1 minute",
                 delay="none",
                 DC=10,
                 cost=100,
                 other="n/a"):

        self.name = name
        self.delivery = delivery
        self.damage = damage
        self.status = status
        self.duration = duration
        self.delay = delay
        self.DC = DC
        self.cost = cost
        self.other = other

    def __repr__(self):
        return "<Poison: %s>"%self.name
    
    def display(self):
        print("%s ..." % self.name)
        attr = self.get_attributes()
        print("  " + "\n  ".join( [ "%10s : %s" % (k, attr[k]) for k in Poison._Attributes[1:]]))

    def get_attributes(self):
        return {'name' : self.name,
                'delivery' : self.delivery,
                'damage' : self.damage,
                'status' : self.status,
                'duration' : self.duration,
                'delay' : self.delay,
                'DC' : self.DC,
                'other' : self.other,
                'cost' : self.cost }
    
    

Poison_list = [

    Poison(
        name="Assassin's Blood",
        delivery="injested",
        damage="1d12",
        status="none",
        duration="1 day",
        DC=10,
        cost=150,
        other="Half damage, no status on success"),

    Poison(
        name="Burnt Othur Fumes",
        delivery="inhaled",
        damage="3d6",
        status="none",
        DC=13,
        cost=500,
        other="Repeat save each turn, 1d6 damage on fail, 3 success to end"),

    
    Poison(
        name="Carrion Crawler Mucus",
        delivery="contact",
        damage="3d6",
        status="poisoned, other",
        DC=13,
        cost=500,
        other="Repeat save each turn, 1d6 damage on fail, 3 success to end"),

    Poison() ]

def input_poison():
    print("Enter the poison's attributes.")
    Attributes = [["name", "A default poison"],
                  ["delivery", "injury"],
                  ["damage", "1d4"],
                  ["status", "none"],
                  ["duration", "1 minute"],
                  ["delay", "none"],
                  ["DC", 1],
                  ["cost", 10],
                  ["other", "n/a"] ]
    for i in range(len(Attributes)):
        prompt_for_attribute(i, Attributes)

    kwargs = dict(Attributes)
    return Poison(**kwargs)
        
def prompt_for_attribute(i, Attributes):
    key, default = Attributes[i]
    inp = input("%s (default `%s`):  "% (key, default))
    if not inp.strip():
        inp = default
    Attributes[i][1] = inp
        
        


# Assassin's blood Ingested 150 gp
# Burnt othur fumes Inhaled 500 gp
# Carrion crawler mucus Contact 200 gp
# Draw poison Injury 200 gp
# Essence of ether Inhaled 300 gp
# Serpent venom Injury 200 gp
# Torpor Ingested 600 gp
# Truth serum Ingested Wyvern poison Injury
# 150 gp
# 1,200 gp

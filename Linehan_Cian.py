# Cian Linehan 119301381
# CS2513 Assignment 1

class Character:
    def __init__(self, name, strength):
        self.__setName(name)
        self.__setStrength(strength)

    def __str__(self):
        return '{} {}'.format(self.__name, self.__strength)

    def __getName(self):
        return self.__name

    def __setName(self, name):
        if name is not None and type(name) == str:
            self.__name = name
        else:
            print('type ERROR')

    def __getStrength(self):
        return self.__strength

    def __setStrength(self, strength):
        if strength is not None and type(strength) not in [float, int]:
            print('type ERROR')
        elif 0 <= strength <= 5:
            self.__strength = float(strength)
        elif strength < 0:
            self.__strength = 0.0
        else:
            self.__strength = 5.0

    name = property(__getName, __setName)
    strength = property(__getStrength, __setStrength)

    def __gt__(self, other):
        return self.__strength > other.__strength

    def fight(self, other):
        if self.__strength > other.__strength:
            self.__setStrength(self.__strength + 1.0)
            print(self)
        elif other.__strength > self.__strength:
            other.__setStrength(other.__strength + 1.0)
            print(other)
        else:
            self.__setStrength(self.__strength - 0.5)
            other.__setStrength(other.__strength - 0.5)


class Orc(Character):
    def __init__(self, name, strength, weapon):
        Character.__init__(self, name, strength)
        self.__setWeapon(weapon)

    def __str__(self):
        return Character.__str__(self) + ' {}'.format(self.__weapon)

    def __getWeapon(self):
        return self.__weapon

    def __setWeapon(self, weapon):
        if weapon is not None and type(weapon) == bool:
            self.__weapon = weapon
        else:
            print('type ERROR')

    weapon = property(__getWeapon, __setWeapon)

    def __gt__(self, other):
        if self.__weapon and not other.__weapon:
            return True
        elif other.__weapon and not self.__weapon:
            return False
        else:
            return Character.__gt__(self, other)

    def fight(self, other):
        if self > other:
            self.strength += 1
            print(self)
        elif other > self:
            other.strength += 1
            print(other)
        else:
            self.strength -= .5
            other.strength -= .5

class Archer(Character):

    def __init__(self, name, strength, kingdom):
        Character.__init__(self, name, strength)
        self.__setKingdom(kingdom)

    def __str__(self):
        return Character.__str__(self) + ' {}'.format(self.__kingdom)

    def __getKingdom(self):
        return self.__kingdom

    def __setKingdom(self, kingdom):
        if kingdom is not None and type(kingdom) == str:
            self.__kingdom = kingdom
        else:
            print('type ERROR')

    kingdom = property(__getKingdom, __setKingdom)

    def fight(self, other):
        if isinstance(other, Orc):
            Character.fight(self, other)
        else:
            print('fight ERROR')


class Knight(Archer):
    def __init__(self, name, strength, kingdom, archers_list):
        Archer.__init__(self, name, strength, kingdom)
        self.__setArchers_list(archers_list)

    def __str__(self):
        rtrn_string = Archer.__str__(self) + ' ['
        # we will not just get the string element of each archer and add it to a list as we do not want quotes around
        # each archer
        for archer in self.__archers_list:
            # if archer is not the last in the list then add a space at the end
            if archer != self.__archers_list[-1]:
                rtrn_string = rtrn_string + archer.__str__() + ', '
            else:
                rtrn_string += archer.__str__()
        return rtrn_string + ']'

    def __getArchers_list(self):
        return self.__archers_list

    def __setArchers_list(self, a_list):
        rtrn_list = []
        if type(a_list) == list:
            for a in a_list:
                # must be an instance of class archer not knight
                if isinstance(a, Archer) and not isinstance(a, Knight):
                    # ignore capitals
                    if a.kingdom.lower() == self.kingdom.lower():
                        rtrn_list.append(a)
                else:
                    print('archers list ERROR')
                    rtrn_list = []
                    break
            self.__archers_list = rtrn_list
        else:
            print('type ERROR')

    archers_list = property(__getArchers_list, __setArchers_list)
o = Orc('cian', 4.3, True)
o2 = Orc('conor', 4.3, False)
a = Archer('conor', 2.1, 'glanmire')
o.fight(a)

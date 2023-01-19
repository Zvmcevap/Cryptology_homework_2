from typing import List, Optional, Dict, Tuple

# Tokovna Šifra
# Vse po modulu 2

# zi = xi + yi, kjer je xi = xi-1 + xi-2 in y = yi-1 + yi -3
# besedilo b1, b2, b3 šifriramo v c1, c2, c3 z ci = bi + zi+2


# 1. Del
# začetni ključ (x1, x2, y0, y1, y2).
zacetni_kljuc = (1, 1, 1, 1, 1)


class TokovniKoder:
    def __init__(self, key: Optional[Tuple[int, int, int, int, int]] = None,
                 b: List[int] = [],
                 c: Optional[List[int]] = None
                 ):
        self.key: Optional[Tuple[int, int, int, int, int]] = key
        self.b: Optional[List[int]] = b
        self.c: Optional[List[int]] = c

        # Da pospešimo rekurzijo
        self.x: Dict[int, int] = {}
        self.y: Dict[int, int] = {}
        self.z: Dict[int, int] = {}

    def get_xi(self, i) -> int:
        if i in self.x:
            return self.x[i]
        if i == 1:
            self.x[i] = self.key[0]
            return self.key[0]
        if i == 2:
            self.x[i] = self.key[1]
            return self.key[1]
        xi = (self.get_xi(i - 1) + self.get_xi(i - 2)) % 2
        self.x[i] = xi
        return xi

    def get_yi(self, i) -> int:
        if i in self.y:
            return self.y[i]
        if i == 0:
            self.y[0] = self.key[2]
            return self.key[2]
        if i == 1:
            self.y[i] = self.key[3]
            return self.key[3]
        if i == 2:
            self.y[i] = self.key[4]
            return self.key[4]
        yi = (self.get_yi(i - 1) + self.get_yi(i - 3)) % 2
        self.y[i] = yi
        return yi

    def get_zi(self, i) -> int:
        xi = self.get_xi(i)
        yi = self.get_yi(i)
        # print(f"x{i} = {xi} y{i} = {yi}")
        zi = (xi + yi) % 2
        # print(f"zi = {zi}")
        self.z[i] = zi
        return zi

    def get_ci(self, i, potential_b=None) -> int:
        if potential_b is None:
            potential_b = self.b[i - 1]
        return (potential_b + self.get_zi(i + 2)) % 2

    def get_key(self):
        # 2⁵ opcij imamo za potencialne ključe kar je izredno mala številka tudi za moj bogi laptop, zato bom kar
        # brute-force pristop naredil:
        for deci_key_value in range(2 ** 5):
            key_has_potential = True
            generated_c = []
            self.y = {}
            self.x = {}
            self.z = {}
            self.key = self.get_key_from_decimal_number(deci=deci_key_value)
            for i in range(1, len(self.b)):
                ci = self.get_ci(i=i)
                generated_c.append(ci)
                if ci != self.c[i - 1]:
                    key_has_potential = False
                    break
            if key_has_potential:
                return

    def get_key_from_decimal_number(self, deci, bits_needed=5):
        binary_string = str(bin(deci)[2:])
        key = [int(bit) for bit in binary_string]
        while len(key) < bits_needed:
            key.insert(0, 0)
        return tuple(key)

    def get_preostanek(self):
        # isti sistem kot pri ugotitvi ključa, 2^(dolžino tajnopisa - dolžino čistopisa) opcij imamo:
        missing_bits = len(self.c) - len(self.b)
        print(missing_bits)
        for preostanek in range(2 ** missing_bits):
            preostanek_has_potential = True
            binarni_tuple = self.get_key_from_decimal_number(deci=preostanek, bits_needed=missing_bits)
            potential_b = self.b.copy() + [i for i in binarni_tuple]
            test_c = self.c[:-missing_bits]
            for i in range(1, len(potential_b) + 1):
                ci = self.get_ci(i=i, potential_b=potential_b[i - 1])
                test_c.append(ci)
                if ci != self.c[i - 1]:
                    preostanek_has_potential = False
                    break
            if preostanek_has_potential:
                return potential_b


def prva_naloga():
    # Input naloge
    zacetni_kljuc = (1, 1, 1, 1, 1)
    tokovni_koder = TokovniKoder(key=zacetni_kljuc)

    # Ne vem koliko členov je potrebnih, zato uporabnikov input:
    stevilo_clenov = None
    while stevilo_clenov is None:
        stevilo_clenov = input("Vpišite željeno število členov ali q za preklic: ")
        if stevilo_clenov == "q":
            return
        if not stevilo_clenov.isdigit():
            stevilo_clenov = None
            print("Vnosa se ne da spremeniti v število")
        else:
            stevilo_clenov = int(stevilo_clenov)
    if stevilo_clenov == "q":
        return

    # Izpiši člene
    for i in range(1, stevilo_clenov + 1):
        tokovni_koder.get_zi(i=i)
    print(f"x = {[tokovni_koder.x[i] for i in range(1, stevilo_clenov + 1)]}")
    print(f"y = {[tokovni_koder.y[i] for i in range(1, stevilo_clenov + 1)]}") # y0 sem izpustil, zato da se členi ujemajo
    print(f"z = {[tokovni_koder.z[i] for i in range(1, stevilo_clenov + 1)]}")


def druga_naloga():
    # Input od naloge
    tajnopis = [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1]
    lepopis = [0, 0, 1, 0, 0, 1, 1, 0, 1, 0]

    tokovni_koder = TokovniKoder(b=lepopis, c=tajnopis)
    tokovni_koder.get_key()
    print(tokovni_koder.key)
    print(tokovni_koder.get_preostanek())
    #     "[0, 0, 1, 0, 0, 1, 1, 0, 1, 0, x, y, z, w" <- pomoč za print
    print("Zadnji štirje členi so --------^--^--^--^")


if __name__ == "__main__":
    prva_naloga()
    druga_naloga()

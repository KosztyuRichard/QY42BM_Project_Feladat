from abc import ABC, abstractmethod
from datetime import datetime


class Jarat(ABC):

    def __init__(self, jaratszam, celallomas, jegy_ar):

        self.__jaratszam = jaratszam
        self.__celallomas = celallomas
        self.__jegy_ar = jegy_ar

    @property
    def jaratszam(self):
        return self.__jaratszam

    @property
    def celallomas(self):
        return self.__celallomas

    @property
    def jegy_ar(self):
        return self.__jegy_ar

    @abstractmethod
    def jarat_tipus(self):
        pass


class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegy_ar):
        super().__init__(jaratszam, celallomas, jegy_ar)

    def jarat_tipus(self):
        return "Belföldi"


class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegy_ar):
        super().__init__(jaratszam, celallomas, jegy_ar)

    def jarat_tipus(self):
        return "Nemzetközi"


class JegyFoglalas:

    def __init__(self, jarat, utas_nev, datum):
        self.__jarat = jarat
        self.__utas_nev = utas_nev
        self.__datum = datum

    @property
    def jarat(self):
        return self.__jarat

    @property
    def utas_nev(self):
        return self.__utas_nev

    @property
    def datum(self):
        return self.__datum

    def __str__(self):
        return f"Utas: {self.__utas_nev}, Járat: {self.__jarat.jaratszam} ({self.__jarat.celallomas}), Dátum: {self.__datum.strftime('%Y-%m-%d')}, Típus: {self.__jarat.jarat_tipus()}"


class LegiTarsasag:

    def __init__(self, nev):
        self.__nev = nev
        self.__jaratok = []
        self.__foglalasok = []

    @property
    def nev(self):
        return self.__nev

    def hozzaad_jarat(self, jarat):
        self.__jaratok.append(jarat)

    def get_jaratok(self):
        return self.__jaratok

    def get_foglalasok(self):
        return self.__foglalasok

    def foglal(self, jaratszam, utas_nev, datum_str):
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
            if datum <= datetime.now():
                raise ValueError("Sajnos a múltba még nem tudunk utazni! :)")
        except ValueError as e:
            return f"\nHiba a foglalás során: Érvénytelen dátum. {e}"
        kivalasztott_jarat = next((j for j in self.__jaratok if j.jaratszam == jaratszam), None)
        if not kivalasztott_jarat:
            return "\nHiba a foglalás során: Nem létezik ilyen járatszám!"

        uj_foglalas = JegyFoglalas(kivalasztott_jarat, utas_nev, datum)
        self.__foglalasok.append(uj_foglalas)
        return f"\nSikeres foglalás! A jegy ára: {kivalasztott_jarat.jegy_ar} Ft."

    def lemond(self, jaratszam, utas_nev):
        for foglalas in self.__foglalasok:
            if foglalas.jarat.jaratszam == jaratszam and foglalas.utas_nev == utas_nev:
                self.__foglalasok.remove(foglalas)
                return f"\nA(z) {jaratszam} járatra szóló foglalás {utas_nev} néven sikeresen törölve."

        return "\nHiba: Nem található ilyen foglalás a rendszerben!"



def main():
    tarsasag = LegiTarsasag("RicsiAirlines")


    tarsasag.hozzaad_jarat(BelfoldiJarat("PA101", "Budapest - Debrecen", 15000))
    tarsasag.hozzaad_jarat(BelfoldiJarat("PA102", "Budapest - Szeged", 18000))
    tarsasag.hozzaad_jarat(NemzetkoziJarat("PA201", "Budapest - London", 65000))


    tarsasag.foglal("PA101", "Keanu Reeves", "2026-06-15")
    tarsasag.foglal("PA101", "Harrison Ford", "2026-06-16")
    tarsasag.foglal("PA102", "Keith Richards", "2026-07-20")
    tarsasag.foglal("PA102", "Morgan Freeman", "2026-07-20")
    tarsasag.foglal("PA201", "Johnny Depp", "2026-08-01")
    tarsasag.foglal("PA201", "Axl Rose", "2026-08-01")


    while True:
        print(f"\n--- {tarsasag.nev} Repülőjegy Foglalási Rendszer ---")
        print("Kérjük, válasszon az alábbi lehetőségek közülL!")
        print("1. Elérhető járatok megtekintése")
        print("2. Jegy foglalása")
        print("3. Foglalás lemondása")
        print("4. Aktuális foglalások listázása")
        print("0. Kilépés")

        valasztas = input("Válassza ki a kívánt menüpontot: ")

        if valasztas == "1":
            print("\n--- Elérhető járatok ---")
            for j in tarsasag.get_jaratok():
                print(
                    f"Járatszám: {j.jaratszam} | Útvonal: {j.celallomas} | Típus: {j.jarat_tipus()} | Ár: {j.jegy_ar} Ft")

        elif valasztas == "2":
            print("\n--- Jegy foglalása ---")
            jaratszam = input("Adja meg a járatszámot: ").upper()
            utas_nev = input("Adja meg az utas nevét: ")
            datum_str = input("Adja meg a dátumot (ÉÉÉÉ-HH-NN formátumban): ")

            eredmeny = tarsasag.foglal(jaratszam, utas_nev, datum_str)
            print(eredmeny)

        elif valasztas == "3":
            print("\n--- Foglalás lemondása ---")
            jaratszam = input("Adja meg a lemondandó járatszámot: ").upper()
            utas_nev = input("Adja meg az utas nevét: ")

            eredmeny = tarsasag.lemond(jaratszam, utas_nev)
            print(eredmeny)

        elif valasztas == "4":
            print("\n--- Aktuális foglalások ---")
            foglalasok = tarsasag.get_foglalasok()
            if not foglalasok:
                print("Jelenleg nincs aktív foglalás a rendszerben.")
            else:
                for idx, f in enumerate(foglalasok, 1):
                    print(f"{idx}. {f}")

        elif valasztas == "0":
            print("Köszönjük, hogy a mi rendszerünket használta!")
            break
        else:
            print("Érvénytelen választás! Kérem, a menüpontok közül válassz (0-4).")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nA program futtatása megszakítva. Sajnáljuk, hogy nem volt elégedett!")
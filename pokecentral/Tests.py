from concurrent.futures import ThreadPoolExecutor as ThreadPool
from json import dump as json_dump

from .Pokemon import Pokemon
from .Utils import POKEMON_NUMBER


class PokeTest:
    @staticmethod
    def _dump_single_mon(id: int) -> None:
        try:
            with open(f"data/pokemons/{id}.json", "w", encoding="utf-8") as outfile:
                pkm = Pokemon(id)
                json_dump(pkm.json(), outfile, ensure_ascii=False, indent=4)
                print(pkm.name)
        except Exception as e:
            print(f"ERROR: {id} -> {e}")
            return id

    @staticmethod
    def dump_all_mon():
        with ThreadPool(20) as executor:
            results = [
                str(i)
                for i in executor.map(
                    PokeTest._dump_single_mon, range(1, POKEMON_NUMBER + 1)
                )
                if i != None
            ]

        with open("private/pkm_down.txt", "w") as f:
            f.writelines(results)

    @staticmethod
    def dump_some_mons():
        with open("private/pkm_down.txt", "r") as f:
            lista = f.readlines()

        while len(lista) != 0:
            id = lista[0]

            print(id)
            pkm = Pokemon(id)
            print(f"\t{pkm.name}")

            with open(f"data/pokemons/{id}.json", "w", encoding="utf-8") as outfile:
                json_dump(pkm.json(), outfile, ensure_ascii=False, indent=4)

            lista.pop(0)

            with open("private/pkm_down.txt", "w") as f:
                f.writelines(lista)

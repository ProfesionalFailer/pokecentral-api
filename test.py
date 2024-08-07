from pokecentral import Pokemon, POKEMON_LIST


"""
for i in range(1, 1009):
    try:
        a = Pokemon(i)
        if "" in a.sprites.keys():
            print(a.name)
    except Exception as E:
        print(f"Pokemon {i} --> Error: {E}")
"""

from pokecentral.Tests import PokeTest

PokeTest.dump_some_mons()

from bs4 import BeautifulSoup
from requests import get as request

from pokecentral.Utils import _POKEHELP
from json import dump as json_dump

dictmon = {
    int(i.find_next("div", {"class": "width-xl-15"}).text.lstrip("#0")): {
        "id": i.find("div", {"class": "width-xl-15"}).text.lstrip("#0"),
        "name": (
            i.find("div", {"class": "text-center width-xl-30"})
            .find_next()
            .text.strip("#")
        ),
        "flat_name": (
            _POKEHELP.flat_name(
                i.find("div", {"class": "text-center width-xl-30"})
                .find_next()
                .text.strip("#")
            )
        ),
        "sprite": (
            request(
                "https://pokeapi.co/api/v2/pokemon/{}".format(
                    i.find("div", {"class": "width-xl-15"}).text.lstrip("#0")
                )
            ).json()["sprites"]
        ),
    }
    for i in BeautifulSoup(
        request(
            "https://wiki.pokemoncentral.it/Elenco_Pok%C3%A9mon_secondo_il_Pok%C3%A9dex_Nazionale"
        ).text,
        "lxml",
    ).find_all("div", {"class": "width-xl-33 width-md-50 width-sm-100"})[:10]
    if "?" not in i.find_next("div", {"class": "width-xl-15"}).text
}

print(dictmon)

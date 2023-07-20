from bs4 import BeautifulSoup
from requests import get as request

from .Exceptions import NotAPokemonException, NotAValidIndexException
from .Utils import (
    POKEMON_LIST,
    POKEMON_NUMBER,
    _POKEHELP,
)


class Pokemon:
    def __init__(self, id: int) -> None:
        """
        Pokemon class base constructor
        :param id: integer between 1 and 1008
        """

        if not str(id).isdigit():
            raise NotAValidIndexException(id)

        if int(id) < 0 or int(id) > POKEMON_NUMBER:
            raise NotAValidIndexException(id)

        self.id = int(id)
        self.name = POKEMON_LIST[self.id - 1]

        self.soup = BeautifulSoup(
            request(
                _POKEHELP.urlencode(f"https://wiki.pokemoncentral.it/{self.name}")
            ).text,
            "lxml",
        )

        self._indices = {
            _POKEHELP.decode(i.find("span", {"class": "toctext"}).text): i.get(
                "href"
            ).strip("#")
            for i in self.soup.find("div", {"id": "toc"}).find("ul").find_all(href=True)
        }

        # Cries are taken from pokemon showdown beacuse on pokemoncentral they aren't available for all pokemons
        self.cry = f"https://play.pokemonshowdown.com/audio/cries/{_POKEHELP.cry_corrector(self.name)}.mp3"

        self._set_abilities()
        self._set_curiosities()
        self._set_dex_entries()
        self._set_egg_groups()
        self._set_height_and_weight()
        self._set_gen()
        self._set_origin_and_name_origin()
        self._set_shape_and_specie()
        self._set_sprites()
        self._set_stats()
        self._set_typing()

    def _set_abilities(self) -> None:
        self.abilities = _POKEHELP.divide_forms(
            {
                _POKEHELP.flat_name(i[0].text)
                if i[0].text.strip("\n ") != ""
                else _POKEHELP.flat_name(self.name): {
                    _POKEHELP.ABILITIES[
                        j.find("div", {"class": "small-text"}).text.lower()
                    ]
                    if j.find("div", {"class": "small-text"}) != None
                    else "primary": j.find_all(href=True)[-1].text
                    for j in i[1].find_all("div", {"class": "width-xl-33 width-xs-50"})
                }
                for i in _POKEHELP.split_by_two(
                    self.soup.find("a", href="/Abilit%C3%A0")
                    .find_parents()[1]
                    .find_next_sibling()
                    .find("div", {"class": "text-center"})
                    .find_all("div", recursive=False)
                )
            }
        )

    def _set_curiosities(self) -> None:
        self.curiosities = [
            _POKEHELP.rmv_sqr_brckts(i.text.replace("\n", "\n\t"))
            for i in (
                self.soup.find("span", {"id": self._indices["curiosita"]})
                .find_parent()
                .find_next("ul")
                .find_all("li")
            )
        ]

    def _set_dex_entries(self) -> None:
        self.dex_entries = {
            _POKEHELP.flat_name(form.find_previous_sibling().text)
            if _POKEHELP.decode(form.find_previous_sibling().text) != "voci pokedex"
            else _POKEHELP.flat_name(self.name): _POKEHELP.split_dex(
                [
                    [
                        _POKEHELP.GAMES[_POKEHELP.decode(sub_game.text.strip("\n"))]
                        for sub_game in game.find_all(
                            "div", {"style": "padding: 0.2em;"}
                        )
                    ]
                    for game in form.find_all("div", {"class": "width-xl-20"})
                ],
                [dex.text for dex in form.find_all("div", {"class": "width-xl-80"})],
            )
            for form in self.soup.find("span", {"id": self._indices["voci pokedex"]})
            .find_parent()
            .find_next_siblings("div", {"class": "width-lg-90"})
        }

    def _set_egg_groups(self) -> None:
        self.egg_groups = [
            i.text
            for i in self.soup.find("a", href="/Gruppi_Uova")
            .find_parent()
            .find_next_sibling()
            .find_all("a")
        ]

    def _set_height_and_weight(self) -> None:
        self.height = {
            (
                _POKEHELP.flat_name(i.split("(")[1])
                if "(" in i
                else _POKEHELP.flat_name(self.name)
            ): i.split("(")[0].strip(" ")
            for i in [
                j
                for j in self.soup.find("a", href="/Elenco_Pok%C3%A9mon_per_altezza")
                .find_parents()[3]
                .find_next_sibling()
                .text.strip(" ")
                .split(")")
                if j != ""
            ]
        }

        self.weight = {
            (
                _POKEHELP.flat_name(i.split("(")[1])
                if "(" in i
                else _POKEHELP.flat_name(self.name)
            ): i.split("(")[0].strip(" ")
            for i in [
                j
                for j in self.soup.find("a", href="/Elenco_Pok%C3%A9mon_per_peso")
                .find_parents()[3]
                .find_next_sibling()
                .text.strip(" ")
                .split(")")
                if j != ""
            ]
        }

    def _set_gen(self) -> None:
        if self.id <= 151:
            self.generation = 1
        elif self.id <= 251:
            self.generation = 2
        elif self.id <= 386:
            self.generation = 3
        elif self.id <= 493:
            self.generation = 4
        elif self.id <= 649:
            self.generation = 5
        elif self.id <= 720:
            self.generation = 6
        elif self.id <= 809:
            self.generation = 7
        elif self.id <= 905:
            self.generation = 8
        else:
            self.generation = 9

    def _set_origin_and_name_origin(self) -> None:
        self.name_origin = _POKEHELP.rmv_sqr_brckts(
            " ".join(
                [
                    i.text.strip(" \n")
                    for i in self.soup.find(
                        "span", {"id": self._indices["origine del nome"]}
                    )
                    .find_parent()
                    .find_next_siblings()
                ]
            ).split("In altre lingue")[0]
        )

        self.origin = _POKEHELP.rmv_sqr_brckts(
            " ".join(
                [
                    i.text.strip(" \n")
                    for i in self.soup.find("span", {"id": self._indices["origine"]})
                    .find_parent()
                    .find_next_siblings()
                ]
            ).split("Origine del nome")[0]
        )

    def _set_shape_and_specie(self) -> None:
        raw_shape = (
            [i for i in self.soup.find_all("b") if "sagoma" in i.text.lower()][0]
            .find_next("img")
            .get("alt")
        )

        if raw_shape in _POKEHELP.SHAPES.keys():
            self.shape = _POKEHELP.SHAPES[raw_shape]
        else:
            self.shape = "None"

        self.specie = self.soup.find("a", href="/Categoria").text

    def _set_sprites(self) -> None:
        self.sprites = {
            (
                _POKEHELP.flat_name(i.text)
                if i.text != ""
                else _POKEHELP.flat_name(self.name)
            ): {
                "default": _POKEHELP.correct_sprite_url(
                    i.find_all("img")[0].get("src")
                ),
                "shiny": _POKEHELP.correct_sprite_url(i.find_all("img")[1].get("src")),
            }
            for i in self.soup.find("span", {"id": self._indices["sprite e modelli"]})
            .find_parent()
            .find_next_siblings()[1]
            .find_all("div", {"style": "padding: 0.1em;"})
            # Eevee companion form and eternal floette don't have a sprite
            if "compagno" not in i.text.lower() and "eterno" not in i.text.lower()
        }

    def _set_stats(self) -> None:
        self.stats = _POKEHELP.divide_forms(
            {
                _POKEHELP.flat_name(i.find_previous("h4").text)
                if i.find_previous("h4").text.lower() != "statistiche di base"
                and i.find_previous("h4").text.lower() != "tutte le forme"
                else _POKEHELP.flat_name(self.name): {
                    _POKEHELP.STATS[
                        j.find_next("td").text.strip(" \n").lower()
                    ]: _POKEHELP.rmv_chars(j.find_all_next("td")[1].text)
                    for j in i.find_next("tr").find_next_siblings()[1:-1]
                    if "totale" not in j.find_next("td").text.lower()
                }
                for i in self.soup.find("span", {"id": self._indices["statistiche"]})
                .find_parent()
                .find_all_next("table", {"class": "text-center"})
            }
        )

        self.stats_sum = {
            i: sum(list(self.stats[i].values())) for i in self.stats.keys()
        }

    def _set_typing(self) -> None:
        self.typing = _POKEHELP.divide_forms(
            {
                (
                    _POKEHELP.flat_name(i.find("div").text)
                    if i.find("div") is not None
                    and "tutte le forme" not in i.text.lower()
                    else _POKEHELP.flat_name(self.name)
                ): list(set([j.text for j in i.find_all("span")]))
                for i in self.soup.find("a", {"href": "/Tipo"})
                .find_parents()[1]
                .find_next_sibling()
                .find_all("div", {"class": "width-xl-50 text-center"})
            }
        )

    def __str__(self) -> str:
        return self.name.capitalize()

    def __repr__(self) -> str:
        return "Pokemon(id={}, name={})".format(self.id, self.name)

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __lt__(self, other) -> bool:
        return self.stats_sum < other.stats_sum

    def json(self) -> dict:
        return {
            "abilities": self.abilities,
            "curiosities": self.curiosities,
            "cry": self.cry,
            "dex_entries": self.dex_entries,
            "egg_groups": self.egg_groups,
            "generation": self.generation,
            "height": self.height,
            "id": self.id,
            "name": self.name,
            "name_origin": self.name_origin,
            "origin": self.origin,
            "shape": self.shape,
            "specie": self.specie,
            "sprites": self.sprites,
            "stats": self.stats,
            "stats_sum": self.stats_sum,
            "types": self.typing,
            "weight": self.weight,
        }

    @classmethod
    def from_name(cls, name=str):
        if name.capitalize() not in POKEMON_LIST:
            raise NotAPokemonException

        id = POKEMON_LIST.index(name) + 1
        return cls(id)

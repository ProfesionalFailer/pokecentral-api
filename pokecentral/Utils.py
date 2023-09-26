from json import load as js_load
from os import path
from re import sub

from unidecode import unidecode

POKECENTRAL_FOLDER = path.dirname(path.realpath(__file__))

with open(
    path.join(POKECENTRAL_FOLDER, "type_chart.json"), "r", encoding="UTF-8"
) as infile:
    TYPE_CHART = js_load(infile)

with open(
    path.join(POKECENTRAL_FOLDER, "pokemon_list.json"), "r", encoding="UTF-8"
) as infile:
    POKEMON_LIST = js_load(infile)

POKEMON_NUMBER = len(POKEMON_LIST)


class _POKEHELP:
    ABILITIES = {
        "prima abilità": "primary",
        "seconda abilità": "secondary",
        "abilità speciale": "hidden",
        "abilità evento": "event",
    }

    GAMES = {
        "rosso": "red",
        "blu": "blue",
        "giallo": "yellow",
        "oro": "gold",
        "argento": "silver",
        "cristallo": "crystal",
        "rubino": "ruby",
        "zaffiro": "sapphire",
        "smeraldo": "emerald",
        "rosso fuoco": "firered",
        "verde foglia": "leafgreen",
        "diamante": "diamond",
        "perla": "pearl",
        "platino": "platinum",
        "heartgold": "heartgold",
        "soulsilver": "soulsilver",
        "nero": "black",
        "bianco": "white",
        "nero 2": "black-2",
        "bianco 2": "white-2",
        "x": "x",
        "y": "y",
        "rubino omega": "omega-ruby",
        "zaffiro alpha": "alpha-sapphire",
        "sole": "sun",
        "luna": "moon",
        "ultrasole": "ultra-sun",
        "ultraluna": "ultra-moon",
        "let's go, pikachu!": "lets-go-pikachu",
        "let's go, eevee!": "lets-go-eevee",
        "spada": "sword",
        "scudo": "shield",
        "diamante lucente": "brilliant-diamond",
        "perla splendente": "shining-pearl",
        "leggende pokemon: arceus": "legends-arceus",
        "scarlatto": "scarlet",
        "violetto": "violet",
    }

    SHAPES = {
        "Body01.png": "testa",
        "Body02.png": "testa e gambe",
        "Body03.png": "pinne",
        "Body04.png": "insettoide",
        "Body05.png": "quadrupede",
        "Body06.png": "due paia di ali",
        "Body07.png": "corpi multipli",
        "Body08.png": "più di 4 arti",
        "Body09.png": "testa e base",
        "Body10.png": "bipedi con coda",
        "Body11.png": "bipedi",
        "Body12.png": "un paio di ali",
        "Body13.png": "serpentiforme",
        "Body14.png": "testa e braccia",
        "BodySconosciuto.png": "sconosciuto",
    }

    STATS = {
        "ps": "hp",
        "attacco": "atk",
        "difesa": "def",
        "att. sp.": "spa",
        "dif. sp.": "spd",
        "velocità": "spe",
    }

    @staticmethod
    def add_name_if(text: str, name: str) -> str:
        if text == "" or text == "-f":
            return name + text
        return text

    @staticmethod
    def decode(index: str) -> str:
        return unidecode(index.lower())

    @staticmethod
    def correct_sprite_url(url: str) -> str:
        return "/".join(
            [sub_url for sub_url in url.split("/")[:-1] if sub_url != "thumb"]
        )

    @staticmethod
    def cry_corrector(name: str):
        return (
            name.lower()
            .replace(" ", "")
            .replace("'", "")
            .replace("♂", "")
            .replace("♀", "-f")
        )

    @staticmethod
    def divide_forms(poke_dict: dict) -> dict:
        return {
            _POKEHELP.flat_name(new_key.strip()): value
            for key, value in poke_dict.items()
            for new_key in key.replace(",", " e ").split(" e ")
        }

    @staticmethod
    def flat_name(name: str) -> str:
        return unidecode(
            name.lower()
            .replace(" ", "-")
            .replace("♂", "")
            .replace("♀", "-f")
            .replace(".", "")
            .replace("é", "e")
            .replace("--", "-")
        ).replace(" ", "")

    @staticmethod
    def rmv_chars(text: str) -> int:
        return int("".join([i for i in text if i.isdigit() and i != ""]))

    @staticmethod
    def rmv_sqr_brckts(text: str) -> str:
        return sub("[\(\[].*?[\)\]]", "", text)

    @staticmethod
    def split_by_two(og_list: list) -> list:
        for i in range(0, len(og_list), 2):
            yield og_list[i : i + 2]

    @staticmethod
    def split_dex(games: list, dexes: list) -> dict:
        return {sub_key: value for key, value in zip(games, dexes) for sub_key in key}

    @staticmethod
    def urlencode(url: str) -> str:
        return (
            url.replace(" ", "_")
            .replace("♂", "%E2%99%82")
            .replace("♀", "%E2%99%80")
            .replace("'", "%27")
        )

const express = require("express");
const path = require("path");
const fs = require("fs");

const app = express(require("express"));
const statuses = require(path.join(__dirname, "data", "statuses.json"));

const pokemonlist = require(path.join(
    __dirname,
    "data",
    "lists",
    "pokemon.json"
));
const max_pokemon = pokemonlist.length;
const validpokemons = pokemonlist.map((x) => flat_name(x["name"]));

function error_text(error_id) {
    return (
        "<h1>Error " +
        statuses[error_id]["status_code"] +
        ": " +
        statuses[error_id]["status"] +
        "</h1><h3>" +
        statuses[error_id]["description"] +
        "</h3>"
    );
}

function flat_name(name) {
    return name
        .toLowerCase()
        .replace(" ", "-")
        .replace("♂", "")
        .replace("♀", "-f");
}

app.get("/pokemon/", (req, res) => {
    var offset = 0;
    var limit = max_pokemon;

    if (req.query.offset >= 0 && parseInt(req.query.offset) < max_pokemon) {
        offset = parseInt(req.query.offset);
    }

    if (req.query.limit > 0 && +req.query.limit <= max_pokemon - offset) {
        limit = parseInt(req.query.limit) + parseInt(offset);
    }

    res.end(JSON.stringify(pokemonlist.slice(offset, limit)));
});

app.get("/pokemon/:id", (req, res) => {
    var id = false;

    if (validpokemons.includes(req.params.id)) {
        id = validpokemons.indexOf(req.params.id) + 1;
    }

    if (req.params.id > 0 && parseInt(req.params.id) < max_pokemon) {
        id = req.params.id;
    }

    if (id === false) {
        res.status(400).send(error_text(400));
        res.end();
    }

    res.header("Content-Type", "application/json");
    res.end(
        JSON.stringify(
            JSON.parse(
                fs.readFileSync(
                    path.join(__dirname, "data", "pokemons", id + ".json")
                )
            )
        )
    );
});

app.get("/*", (req, res) => {
    res.status(400).send(error_text(400));
    res.end();
});

app.listen(3000);
/* Variables */
const pokeimg = new Image();

let point_loss = 0;
let points_now = 20;
let pokemon;

let valid_mons;
let options;

function flat_name(name) {
	console.log(name);
	return name.toLowerCase().replace(" ", "-").replace("♂", "").replace("♀", "-f").replace(".", "").replace("é", "e");
}

fetch("/pokemon")
	.then((res) => res.json())
	.then((out) => {
		valid_mons = out.map((x) => x["flat_name"]);
		options = out.map((x) => x["name"]);
	})

	.catch((err) => {
		throw err;
	});

const points_losses = {
	types: 5,
	pokedex: 4,
	egg: 2,
	dimension: 2,
	shape: 1,
	specie: 7,
	abilities: 5,
	stats: 2,
};

const hint_texts = {
	types: "Tipi",
	pokedex: "Numero Pokedex",
	egg: "Gruppo Uova",
	dimension: "Dimensioni",
	shape: "Forma",
	specie: "Specie",
	abilities: "Abilità",
	stats: "Somma Statistiche",
};

class Pokemon {
	constructor(id) {
		fetch("/pokemon/" + id)
			.then((res) => res.json())
			.then((mondata) => {
				this.mondata = mondata;
				this.flat_name = mondata["flat_name"];

				this.abilities = Object.values(mondata["abilities"][this.flat_name]).join(", ");
				this.cry = mondata["cry"];
				this.dimension = `${mondata["height"][this.flat_name]}, ${mondata["weight"][this.flat_name]}`;
				this.egg = mondata["egg_groups"].join(", ");
				this.entries = Object.values(mondata["dex_entries"])
					.map((entry) => Object.values(entry))
					.flat();
				this.id = id;
				this.name = mondata["name"];
				this.pokedex = "#" + id;
				this.shape = mondata["shape"];
				this.specie = mondata["specie"];
				this.sprite = mondata["sprites"][this.flat_name]["default"];
				this.stats = "Totale: " + mondata["stats_sum"][this.flat_name];
				this.types = mondata["types"][this.flat_name].join(", ");
			})
			.then(() => {
				document.getElementById("dex_entry").innerHTML = this.get_dex();
				pokeimg.src = this.sprite;
			})

			.catch((err) => {
				throw err;
			});
	}

	get_dex() {
		return this.entries[Math.floor(Math.random() * this.entries.length)].replace(RegExp(this.name, "ig"), "???");
	}
}

/* Local Storage */
if (localStorage.getItem("total_points") === null) {
	localStorage.setItem("total_points", 0);
}

function set_points(new_points) {
	localStorage.setItem("total_points", new_points);
}

function show_points() {
	document.getElementById("points_text").innerHTML = "Punti Totali: " + localStorage.getItem("total_points");
}

/* Game Functions */
function game_start() {
	points_now = 20;
	points_loss = 0;

	show_points();

	document.getElementById("sprite").src = "question.png";
	document.getElementById("game").innerHTML = "???";

	pokemon = new Pokemon(Math.floor(Math.random() * 1007));
}

function show_info(element) {
	point_loss = points_losses[element.getAttribute("id")];

	if (points_now - point_loss <= 0) {
		alert("Non hai abbastanza punti per usare questo indizio");
		return;
	}

	element.classList.add("btn-outline-primary");
	element.classList.remove("btn-primary");
	element.innerHTML = pokemon[element.getAttribute("id")];

	points_now -= point_loss;
}

function guess() {
	if (document.getElementById("user_guess").value == "") {
		return;
	}

	if (!valid_mons.includes(flat_name(document.getElementById("user_guess").value))) {
		alert("Il pokemon inserito non è valido!");
		document.getElementById("user_guess").value = "";
		return;
	}

	if (pokemon.flat_name == flat_name(document.getElementById("user_guess").value)) {
		document.getElementById("user_guess").value = "";
		game_end();
		return;
	}

	document.getElementById("user_guess").value = "";
	points_now -= 1;

	if (points_now > 0) {
		alert("Sbagliato");
		return;
	}

	game_end();
}

function game_end() {
	document.getElementById("game").innerHTML = pokemon.name;
	document.getElementById("sprite").src = pokeimg.src;

	let message;
	let new_points;

	if (points_now > 0) {
		message = "Hai indovinato!";
		new_points = parseInt(localStorage.getItem("total_points")) + parseInt(points_now);
	} else {
		message = "Hai perso!";
		new_points = 0;
	}

	set_points(new_points);

	setTimeout(() => {
		alert(message);
		for (const [key, value] of Object.entries(hint_texts)) {
			document.getElementById(key).innerHTML = value;
			document.getElementById(key).classList.remove("btn-outline-primary");
			document.getElementById(key).classList.add("btn-primary");
		}
		game_start();
	}, 1250);
}

/* Event Listeners */
document.getElementById("user_guess").addEventListener("keypress", (event) => {
	if (event.key === "Enter") {
		guess();
	}
});

game_start();

import nameparser

names = [
    "Paixão, Geraldo Ferreira da",
    "Miranda Álvarez, Rita Berenice",
    "McQuerry, Maureen, 1955-",
    "Widmer, Thomas, 1962-",
    "Schulze, Petra, 1965-",
    "Canali, Roger, 1961-",
    "Ammann, Paul, 1957-",
    "Endler, Dirk",
    "Drausch, Valentin, 1546-1610?",
    "Dress, Andreas, 1943-",
    "Mai, Kurt",
    "Tschuppik, Wolf-Michael Oliver",
    "Gugler, Andreas, 1958-",
    "Grulke, Markus",
    "Gerboth, Gesine",
    "Müller, Anna Maria",
    "Richardson, Lynn, 1942-",
    "Chen, Arthur H.",
    "Pember, Ann, 1946-",
    "Pasanella, Marco, 1962-",
    "Siegel, Jonah, 1963-",
    "Newson, Lisa",
    "Cohen, Margo",
    "Cohen, Maurice",
    "Brennan, Michael",
    "Peter, Bruce",
    "Griff, Dean",
    "Schwartz, Rodney",
    "Jeroch, Heinz",
    "Weström, Ute",
    "Schopp-Guth, Armin",
    "Lang, Günter, 1964-",
    "Suttner, Wolfgang",
    "Kern, Angelika",
    "Kern, Andreas",
    "Lauerwald, Tom",
    "Ruhm, Constanze, 1965-",
    "Bayer, Andreas",
    "Löbner, Anna",
    "Comani, Daniela, 1965-",
    "Daniel, Beate, 1966-",
    "Nelson, Felicitas H.",
    "Krebs-Thulin, Rosa",
    "Häsler, Albert",
    "Köhler, Max, 1942-",
    "Heine, Wilhelm, 1871-1917",
    "Korsaks, P. (Pēteris)",
]


def main():
    for name in names:
        print(nameparser.HumanName(name).as_dict())


if __name__ == "__main__":
    main()

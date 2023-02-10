from countries import Continent, Country, continents, countries


def test_country_list():
    assert len(countries) == 249
    assert isinstance(list(countries)[0], Country)


def test_get_country_by_code():
    country = countries.get(code="IT")

    assert country
    assert country.name == "Italy"
    assert country.code == "IT"
    assert country.continent.code == "EU"
    assert country.continent.name == "Europe"


def test_get_country_by_multiple_arguments():
    country = countries.get(name="Italy", code="IT")

    assert country
    assert country.name == "Italy"


def test_country_not_found():
    assert countries.get(name="Scandinavia") is None


def test_continents_list():
    assert len(continents) == 7
    assert isinstance(list(continents)[0], Continent)


def test_get_continent_by_code():
    continent = continents.get(code="EU")

    assert continent
    assert continent.name == "Europe"
    assert continent.code == "EU"


def test_get_continent_by_multiple_arguments():
    continent = continents.get(name="Europe", code="EU")

    assert continent
    assert continent.code == "EU"


def test_continent_not_found():
    assert continents.get(name="Narnia") is None


def test_filter_countries_by_continent():
    european_countries = countries.filter(continent="EU")

    assert len(list(european_countries)) == 52

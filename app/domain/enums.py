from enum import Enum, StrEnum


class Sport(StrEnum):
    FOOTBALL = "football"
    NBA = "nba"


class League(StrEnum):
    # nba
    NBA = "NBA"
    # america
    BRASILEIRAO = "Brasileirao"
    ARGENTINA_PRIMERA = "Liga Profesional"
    CHILE_PRIMERA = "Liga de Primera"
    PARAGUAY_PRIMERA = "Division de Honor"
    COLOMBIA_PRIMERA = "Liga DIMAYOR"
    ECUADOR_SERIE_A = "LigaPro"
    # europe
    PREMIER_LEAGUE = "Premier League"
    LA_LIGA = "La Liga"
    BUNDESLIGA = "Bundesliga"
    SERIE_A = "Serie A"
    LIGUE_1 = "Ligue 1"


class Conference(Enum):
    EASTERN = "Eastern"
    WESTERN = "Western"


class Nationality(Enum):
    # america
    ARGENTINA = "Argentina"
    BRAZIL = "Brazil"
    CHILE = "Chile"
    PARAGUAY = "Paraguay"
    ECUADOR = "Ecuador"
    COLOMBIA = "Colombia"
    VENEZUELA = "Venezuela"
    URUGUAY = "Uruguay"
    PERU = "Peru"
    BOLIVIA = "Bolivia"
    # europe
    ENGLAND = "England"
    SPAIN = "Spain"
    ITALY = "Italy"
    FRANCE = "France"
    GERMANY = "Germany"
    PORTUGAL = "Portugal"
    HOLLAND = "Holland"
    TURKEY = "Turkey"
    BELGIUM = "Belgium"

from enum import Enum

class Team(Enum):
    ANA = "ANA"
    ARI = "ARI"
    BOS = "BOS"
    BUF = "BUF"
    CAR = "CAR"
    CBJ = "CBJ"
    CGY = "CGY"
    CHI = "CHI"
    COL = "COL"
    DAL = "DAL"
    DET = "DET"
    EDM = "EDM"
    FLA = "FLA"
    LAK = "LAK"
    MIN = "MIN"
    MTL = "MTL"
    NJD = "NJD"
    NSH = "NSH"
    NYI = "NYI"
    NYR = "NYR"
    OTT = "OTT"
    PHI = "PHI"
    PIT = "PIT"
    SEA = "SEA"
    SJS = "SJS"
    STL = "STL"
    TBL = "TBL"
    TOR = "TOR"
    UTA = "UTA"
    VAN = "VAN"
    VGK = "VGK"
    WPG = "WPG"
    WSH = "WSH"

    @property
    def full_name(self) -> str:
        return TEAM_TO_FULL_NAME[self]

FULL_NAME_TO_TEAM = {
    "ANAHEIM DUCKS": Team.ANA,
    "ARIZONA COYOTES": Team.ARI,
    "BOSTON BRUINS": Team.BOS,
    "BUFFALO SABRES": Team.BUF,
    "CAROLINA HURRICANES": Team.CAR,
    "COLUMBUS BLUE JACKETS": Team.CBJ,
    "CALGARY FLAMES": Team.CGY,
    "CHICAGO BLACKHAWKS": Team.CHI,
    "COLORADO AVALANCHE": Team.COL,
    "DALLAS STARS": Team.DAL,
    "DETROIT RED WINGS": Team.DET,
    "EDMONTON OILERS": Team.EDM,
    "FLORIDA PANTHERS": Team.FLA,
    "LOS ANGELES KINGS": Team.LAK,
    "MINNESOTA WILD": Team.MIN,
    "MONTREAL CANADIENS": Team.MTL,
    "MONTRÉAL CANADIENS": Team.MTL,
    "NEW JERSEY DEVILS": Team.NJD,
    "NASHVILLE PREDATORS": Team.NSH,
    "NEW YORK ISLANDERS": Team.NYI,
    "NEW YORK RANGERS": Team.NYR,
    "OTTAWA SENATORS": Team.OTT,
    "PHILADELPHIA FLYERS": Team.PHI,
    "PITTSBURGH PENGUINS": Team.PIT,
    "SAN JOSE SHARKS": Team.SJS,
    "SEATTLE KRAKEN": Team.SEA,
    "ST. LOUIS BLUES": Team.STL,
    "TAMPA BAY LIGHTNING": Team.TBL,
    "TORONTO MAPLE LEAFS": Team.TOR,
    "UTAH MAMMOTH": Team.UTA,
    "VANCOUVER CANUCKS": Team.VAN,
    "VEGAS GOLDEN KNIGHTS": Team.VGK,
    "WINNIPEG JETS": Team.WPG,
    "WASHINGTON CAPITALS": Team.WSH,
}

TEAM_TO_FULL_NAME = {
    Team.ANA: "Anaheim Ducks",
    Team.ARI: "Arizona Coyotes",
    Team.BOS: "Boston Bruins",
    Team.BUF: "Buffalo Sabres",
    Team.CAR: "Carolina Hurricanes",
    Team.CBJ: "Columbus Blue Jackets",
    Team.CGY: "Calgary Flames",
    Team.CHI: "Chicago Blackhawks",
    Team.COL: "Colorado Avalanche",
    Team.DAL: "Dallas Stars",
    Team.DET: "Detroit Red Wings",
    Team.EDM: "Edmonton Oilers",
    Team.FLA: "Florida Panthers",
    Team.LAK: "Los Angeles Kings",
    Team.MIN: "Minnesota Wild",
    Team.MTL: "Montréal Canadiens",
    Team.NJD: "New Jersey Devils",
    Team.NSH: "Nashville Predators",
    Team.NYI: "New York Islanders",
    Team.NYR: "New York Rangers",
    Team.OTT: "Ottawa Senators",
    Team.PHI: "Philadelphia Flyers",
    Team.PIT: "Pittsburgh Penguins",
    Team.SEA: "Seattle Kraken",
    Team.SJS: "San Jose Sharks",
    Team.STL: "St. Louis Blues",
    Team.TBL: "Tampa Bay Lightning",
    Team.TOR: "Toronto Maple Leafs",
    Team.UTA: "Utah Mammoth",
    Team.VAN: "Vancouver Canucks",
    Team.VGK: "Vegas Golden Knights",
    Team.WPG: "Winnipeg Jets",
    Team.WSH: "Washington Capitals",
}

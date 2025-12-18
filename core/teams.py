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
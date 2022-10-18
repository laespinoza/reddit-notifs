SUBREDDIT = "watchexchange"
NUM_POSTS = 5
SLEEP_TIMER = 60.0  # 60.0 = 1min
"""
The following tuple contains:
    1. list of required terms/stems, 
    2. list of secondary terms,
    3. min number of secondary terms needed to be a match
"""
KEYWORDS_GROUP_OMEGA = (
    ["omega"],
    [
        "speedmaster",
        "moon",
        "sandwich",
        "sapphire",
        "hesalite",

        # DSotM
        "meteorite",
        "311.63.44.51.99.001",

        # cal 3861
        "3861",
        # hesalite ~ $4750 - $5500
        "001", "310.30.42.50.01.001",
        # sapphire ~ $5500 - $6300
        "002", "310.30.42.50.01.002",

        # cal 1863 (similar to 1861, decorated and designed for exhibition caseback)
        "1863",
        # sapphire ~ $4750 - 4900
        "006", "311.30.42.30.01.006",
        # older ref ~ $3800 - $4300
        "35735000", "3573.50", "3573.50.00", "3573",
        # hesalite sandwich
        "35725000", "3572.50", "3572.50.00", "3572",

        # cal 1861 (cal worn on moon)
        "1861",
        # hesalite
        "005", "311.30.42.30.01.005",
        # older ref
        "35705000", "3570.50", "3570.50.00", "3570",
    ],
    2,
)
KEYWORDS_GROUP_ZELOS = (
    ["zelos"],
    [
        "meteorite",
        "meteor",
    ],
    2,
)
KEYWORDS_GROUP_MISC = (
    [],
    [
        "meteorite",
        "meteor",
        "skeleton",
        "heart",
    ],
    1
)
KEYWORD_GROUPS = [KEYWORDS_GROUP_OMEGA, KEYWORDS_GROUP_ZELOS, KEYWORDS_GROUP_MISC]

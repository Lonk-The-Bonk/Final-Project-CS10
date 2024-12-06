import os

WIDTH=1000
HEIGHT=680
FPS=30

Background_Color=(168, 218, 220)


Resources_Path="Assets"
Images_Path = os.path.join(Resources_Path,"Images")
Sounds_Path = os.path.join(Resources_Path,"Sounds")
Fonts_Path = os.path.join(Resources_Path,"Fonts")

BOARD={
    0:{
        "Type":"GO"
    },
    1:{
        "Type":"Street",
        "Name":"Vine Street",
        "Color":"Brown",
        "Price":60,
        "Rent":2,
        "House1":30,
        "House2":50,
        "House3":90,
        "House4":160,
        "Hotel":250,
        "House_Cost":50,
        "Mortgage":30
    },
    2:{
        "Type":"Community Chest"
    },
    3:{
        "Type":"Street",
        "Name":"Coventry Street",
        "Color":"Brown",
        "Price":60,
        "Rent":2,
        "House1":20,
        "House2":60,
        "House3":180,
        "House4":320,
        "Hotel":450,
        "House_Cost":50,
        "Mortgage":30
    },
    4:{
        "Type":"Tax",
        "Fee":25
    },
    5:{
        "Type":"RailRoad",
        "Name":"Marylebone Station",
        "Price":200,
        "station1":25,
        "station2":50,
        "station3":100,
        "station4":200
        
        
    },
    6:{
        "Type":"Street",
        "Name":"Leicester Square",
        "Color":"Blue",
        "Price":100,
        "Rent":6,
        "House1":30,
        "House2":90,
        "House3":270,
        "House4":400,
        "Hotel":550,
        "House_Cost":50,
        "Mortgage":50
    },
    7:{
        "Type":"Chance"
    },
    8:{
        "Type":"Street",
        "Name":"Bow Street",
        "Color":"Blue",
        "Price":100,
        "Rent":6,
        "House1":30,
        "House2":90,
        "House3":270,
        "House4":400,
        "Hotel":550,
        "House_Cost":50,
        "Mortgage":50
        
    },
    9:{
        "Type":"Street",
        "Name":"WhiteChapel Street",
        "Color":"Blue",
        "Price":120,
        "Rent":8,
        "House1":40,
        "House2":100,
        "House3":300,
        "House4":450,
        "Hotel":600,
        "House_Cost":50,
        "Mortgage":60
    },
    10:{
        "Type":"Jail"
    },
    11:{
        "Type":"Street",
        "Name":"The Angel Islington",
        "Color":"Pink",
        "Price":300,
        "Rent":26,
        "House1":130,
        "House2":390,
        "House3":900,
        "House4":1100,
        "Hotel":1275,
        "House_Cost":200,
        "Mortgage":150
    },
    12:{
        "Type":"Utility",
        "Name":"Electric Company",
        "Price":150,
        "company1":4,
        "company2":10,
    },
    13:{
        "Type":"Street",
        "Name":"Trafalgar Square",
        "Color":"Pink",
        "Price":350,
        "Rent":35,
        "House1":175,
        "House2":500,
        "House3":1100,
        "House4":1300,
        "Hotel":1500,
        "House_Cost":200,
        "Mortgage":150
    },
    14:{
        "Type":"Street",
        "Name":"Northumberland Avenue",
        "Color":"Pink",
        "Price":320,
        "Rent":26,
        "House1":150,
        "House2":450,
        "House3":1000,
        "House4":1200,
        "Hotel":1400,
        "House_Cost":200,
        "Mortgage":160
    },
    15:{
        "Type":"RailRoad",
        "Name":"Fenchurch Street Station ",
        "Price":200,
        "station1":25,
        "station2":50,
        "station3":100,
        "station4":200
    },
    16:{
        "Type":"Street",
        "Name":"Marlborough Street",
        "Color":"Orange",
        "Price":140,
        "Rent":10,
        "House1":50,
        "House2":150,
        "House3":450,
        "House4":652,
        "Hotel":750,
        "House_Cost":100,
        "Mortgage":70
        
    },
    17:{
        "Type":"Community Chest"
    },
    18:{
        "Type":"Street",
        "Name":"Fleet Street",
        "Color":"Orange",
        "Price":140,
        "Rent":10,
        "House1":50,
        "House2":150,
        "House3":450,
        "House4":625,
        "Hotel":750,
        "House_Cost":100,
        "Mortgage":70
    },
    19:{
        "Type":"Street",
        "Name":"Old Kent Road",
        "Color":"Orange",
        "Price":120,
        "Rent":8,
        "House1":60,
        "House2":180,
        "House3":500,
        "House4":700,
        "Hotel":900,
        "House_Cost":100,
        "Mortgage":80
    },
    20:{
        "Type":"Free Parking"
    },
    21:{
        "Type":"Street",
        "Name":"White Hall",
        "Color":"Red",
        "Price":300,
        "Rent":26,
        "House1":130,
        "House2":390,
        "House3":900,
        "House4":1100,
        "Hotel":1275,
        "House_Cost":200,
        "Mortgage":150
    },
    22:{
        "Type":"Chance"
    },
    23:{
        "Type":"Street",
        "Name":"Pentonville Road",
        "Color":"Red",
        "Price":350,
        "Rent":35,
        "House1":175,
        "House2":500,
        "House3":1100,
        "House4":1300,
        "Hotel":1500,
        "House_Cost":200,
        "Mortgage":150
    },
    24:{
        "Type":"Street",
        "Name":"Pall Mall",
        "Color":"Red",
        "Price":320,
        "Rent":26,
        "House1":150,
        "House2":450,
        "House3":1000,
        "House4":1200,
        "Hotel":1400,
        "House_Cost":200,
        "Mortgage":160
    },
    25:{
        "Type":"RailRoad",
        "Name":"King Cross Station",
        "Price":200,
        "station1":25,
        "station2":50,
        "station3":100,
        "station4":200
    },
    26:{
        "Type":"Street",
        "Name":"Bond Street",
        "Color":"Yellow",
        "Price":260,
        "Rent":22,
        "House1":110,
        "House2":330,
        "House3":800,
        "House4":975,
        "Hotel":1150,
        "House_Cost":150,
        "Mortgage":130
    },
    27:{
        "Type":"Street",
        "Name":"Strand",
        "Color":"Yellow",
        "Price":260,
        "Rent":22,
        "House1":110,
        "House2":330,
        "House3":800,
        "House4":975,
        "Hotel":1150,
        "House_Cost":150,
        "Mortgage":130
    },
    28:{
        "Type":"Utility",
        "Name":"Water Works",
        "Price":150,
        "company1":4,
        "company2":10
    },
    29:{
        "Type":"Street",
        "Name":"Regent Street",
        "Color":"Yellow",
        "Price":280,
        "Rent":24,
        "House1":120,
        "House2":360,
        "House3":850,
        "House4":1025,
        "Hotel":1200,
        "House_Cost":150,
        "Mortgage":140
    },
    30:{
        "Type":"Go To Jail"
    },
    31:{
        "Type":"Street",
        "Name":"Easton Road",
        "Color":"Green",
        "Price":180,
        "Rent":14,
        "House1":70,
        "House2":200,
        "House3":550,
        "House4":700,
        "Hotel":900,
        "House_Cost":100,
        "Mortgage":90
    },
    32:{
        "Type":"Street",
        "Name":"Piccadilly",
        "Color":"Green",
        "Price":180,
        "Rent":14,
        "House1":70,
        "House2":200,
        "House3":550,
        "House4":700,
        "Hotel":950,
        "House_Cost":100,
        "Mortgage":90
    },
    33:{
        "Type":"Community Chest"
    },
    34:{
        "Type":"Street",
        "Name":"Oxford Street",
        "Color":"Green",
        "Price":200,
        "Rent":16,
        "House1":80,
        "House2":220,
        "House3":600,
        "House4":800,
        "Hotel":1000,
        "House_Cost":100,
        "Mortgage":100
    },
    35:{
        "Type":"RailRoad",
        "Name":"Liverpool Street Station",
        "Price":200,
        "station1":25,
        "station2":50,
        "station3":100,
        "station4":200
    },
    36:{
        "Type":"Chance"
    },
    37:{
        "Type":"Street",
        "Name":"Park Lane",
        "Color":"Dark Blue",
        "Price":350,
        "Rent":35,
        "House1":175,
        "House2":500,
        "House3":1100,
        "House4":1300,
        "Hotel":1500,
        "House_Cost":200,
        "Mortgage":175
    },
    38:{
        "Type":"Tax",
        "Fee":75
    },
    39:{
        "Type":"Street",
        "Name":"Mayfair",
        "Color":"Dark Blue",
        "Price":400,
        "Rent":50,
        "House1":200,
        "House2":600,
        "House3":1400,
        "House4":1700,
        "Hotel":2000,
        "House_Cost":200,
        "Mortgage":200
    },
    
}

Chance_Cards = {}
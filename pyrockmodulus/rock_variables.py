# /////////////////////////////////////////////////////////////// #
# Python Script initially created on 2022-12-15
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2022
# Created using PyCharm
# /////////////////////////////////////////////////////////////// #

# Dictionary to hold Rock Category
_rocktype_dictionary = {
    "Diabase": ["Igneous", 'blue', 'ID'],
    "Intrusive Rock": ["Igneous", 'black', "IG"],
    "Flow Rock": ["Igneous", 'red', "IF"],
    "Granite": ["Igneous", 'black', "IG"],
    "Basalt": ["Igneous", 'red', "IF"],
    "Quartzite": ["Metamorphic", 'orange', "MQ"],
    "Gneiss": ["Metamorphic", 'yellow', "MG"],
    "Marble": ["Metamorphic", 'purple', "MM"],
    "Schist_Flat": ["Metamorphic", 'darkgreen', "MSpp"],
    "Schist": ["Metamorphic", 'darkgreen', "MS"],
    "Schist_Perp": ["Metamorphic", 'olive', "MSpl"],
    "Limestone": ["Sedimentary", 'cyan', "SL"],
    "Mudstone": ["Sedimentary", 'grey', "SSh"],
    "Sandstone": ["Sedimentary", 'brown', "SS"],
    "Shale": ["Sedimentary", 'dodgerblue', 'SSh'],
    "Chalk": ["Sedimentary", 'fuchsia', 'SC']
}

_poisson_density_range = [
    {'Rock Type': 'Andesite', 'Group': 'Igneous', 'Min_P': 0.2, 'Max_P': 0.35, 'Min_D': 2.172, 'Max_D': 3.052},
    {'Rock Type': 'Basalt', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.35, 'Min_D': 0.736, 'Max_D': 3.124},
    {'Rock Type': 'Claystone', 'Group': 'Sedimentary', 'Min_P': 0.25, 'Max_P': 0.4, 'Min_D': 1.8, 'Max_D': 2.2},
    {'Rock Type': 'Conglomerate', 'Group': 'Sedimentary', 'Min_P': 0.1, 'Max_P': 0.4, 'Min_D': 2.47, 'Max_D': 2.76},
    {'Rock Type': 'Diabase/Dolerite', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.35, 'Min_D': 2.296, 'Max_D': 3.19},
    {'Rock Type': 'Diorite', 'Group': 'Igneous', 'Min_P': 0.2, 'Max_P': 0.3, 'Min_D': 2.03, 'Max_D': 3.124},
    {'Rock Type': 'Dolomite', 'Group': 'Sedimentary', 'Min_P': 0.15, 'Max_P': 0.35, 'Min_D': 2.4, 'Max_D': 2.85},
    {'Rock Type': 'Gabbro', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.38, 'Min_D': 2.7, 'Max_D': 3.19},
    {'Rock Type': 'Gneiss', 'Group': 'Metamorphic', 'Min_P': 0.1, 'Max_P': 0.3, 'Min_D': 2.064, 'Max_D': 3.36},
    {'Rock Type': 'Granite', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.33, 'Min_D': 2.4, 'Max_D': 2.785},
    {'Rock Type': 'Granodiorite', 'Group': 'Igneous', 'Min_P': 0.15, 'Max_P': 0.25, 'Min_D': 2.63, 'Max_D': 2.74},
    {'Rock Type': 'Greywacke', 'Group': 'Sedimentary', 'Min_P': 0.08, 'Max_P': 0.23, 'Min_D': 2.41, 'Max_D': 2.77},
    {'Rock Type': 'Limestone', 'Group': 'Sedimentary', 'Min_P': 0.1, 'Max_P': 0.33, 'Min_D': 1.31, 'Max_D': 2.92},
    {'Rock Type': 'Marble', 'Group': 'Metamorphic', 'Min_P': 0.15, 'Max_P': 0.3, 'Min_D': 2.64, 'Max_D': 3.02},
    {'Rock Type': 'Marl', 'Group': 'Sedimentary', 'Min_P': 0.13, 'Max_P': 0.33, 'Min_D': 1.86, 'Max_D': 2.69},
    {'Rock Type': 'Norite', 'Group': 'Igneous', 'Min_P': 0.2, 'Max_P': 0.25, 'Min_D': 2.72, 'Max_D': 3.02},
    {'Rock Type': 'Quartzite', 'Group': 'Metamorphic', 'Min_P': 0.1, 'Max_P': 0.33, 'Min_D': 2.55, 'Max_D': 3.05},
    {'Rock Type': 'Rock Salt', 'Group': 'Sedimentary', 'Min_P': 0.05, 'Max_P': 0.3, 'Min_D': 2.1, 'Max_D': 2.9},
    {'Rock Type': 'Sandstone', 'Group': 'Sedimentary', 'Min_P': 0.05, 'Max_P': 0.4, 'Min_D': 1.44, 'Max_D': 2.8},
    {'Rock Type': 'Shale', 'Group': 'Sedimentary', 'Min_P': 0.05, 'Max_P': 0.32, 'Min_D': 1.6, 'Max_D': 2.92},
    {'Rock Type': 'Siltstone', 'Group': 'Sedimentary', 'Min_P': 0.13, 'Max_P': 0.35, 'Min_D': 1.11, 'Max_D': 2.87},
    {'Rock Type': 'Tuff', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.28, 'Min_D': 1.6, 'Max_D': 2.78}
]




def ucs_strength_criteria(type):
    """
    ## Insert all UCS Strength Criterion Here.     ## ALL VALUES ARE IN MPa
    # Name Format {Reference Name: [Name of Category]}
    # Value Format {Reference Name: [Boundaries Location]}  <=> in MPa
    # converted_psi [Reference name that are converted from psi to MPa]

    :param type: rock classification system to load
    :type type: str

    :return:
    :rtype:
    """

    category_names = {'ISRM\n1977': ['Extremely\nweak', 'Very weak', 'Weak', 'Moderately\nweak', 'Medium\nstrong', 'Strong', 'Very strong', 'Extremely strong'],
                      'ISRMCAT\n1979': ['R0','R1','R2','R3','R4','R5','R6'],
                      'Bieniawski\n1974': ['Very Low', 'Low', 'Medium', 'High', 'Very high'],
                      'Jennings\n1973': ['Very soft', 'Soft', 'Hard', 'Very hard', 'Extremely hard'],
                      'Broch & Franklin\n1972': ['Very low', 'Low', 'Medium', 'High', 'Very high', 'Extremely high'],
                      'Geological Society\n1970': ['Very weak', 'Weak', 'Moderately weak', 'Moderately\nstrong', 'Strong', 'Very strong', 'Extremely strong'],
                      'Deere & Miller\n1966':['Very low (E)', 'Low (D)', 'Medium (C)', 'High (B)', 'Very high (A)'],
                      'Coates\n1964': ['Weak', 'Strong', 'Very strong'],
                      'Coates & Parsons\n1966': ['Weak', 'Strong', 'Very strong'],
                      'ISO 14689\n2017':['Extremely\nweak', 'Very weak', 'Weak', 'Moderately\nweak', 'Medium\nstrong', 'Strong', 'Very strong', 'Extremely strong'],
                      'Anon\n1977':['Very weak','Weak','Moderately Weak','Moderately Strong','Strong','Very Strong'],
                      'Anon\n1979':['Weak','Moderately Strong','Strong','Very Strong', 'Extremely Strong'],
                      'Ramamurthy\n2004':['Very Low (F)','Low (E)', 'Medium (D)', 'Moderate (C)', 'High (B)', 'Very High (A)']}

    category_values = {'ISRM\n1977': [0.25, 1, 5, 25, 50, 100, 250, 1000],
                        'ISRMCAT\n1979': [0.25, 1, 5, 25, 50, 100, 250, 1000],
                        'Bieniawski\n1974': [1, 25, 50, 100, 200, 1000],
                        'Jennings\n1973': [0.7, 3, 10, 20, 70, 1000],
                        'Broch & Franklin\n1972': [0.8, 2.5, 7, 25, 70, 250, 1000],
                        'Geological Society\n1970': [1.25, 5, 12.5, 50, 100, 200, 1000],
                        'Deere & Miller\n1966': [0.6, 27.5, 55.1, 110.3, 220.6, 1000],
                        'Coates\n1964': [0.6, 34.4, 172, 1000],
                        'Coates & Parsons\n1966': [0.6, 68.9, 172, 1000],
                        'ISO 14689\n2017': [0.6, 1, 5, 12.5, 25, 50, 100, 250, 1000],
                        'Anon\n1977': [0.6, 1.25, 5, 12.5, 50, 100, 1000],
                        'Anon\n1979': [1.5, 15, 50, 120, 230, 1000],
                        'Ramamurthy\n2004':[0.8, 5, 25, 50, 100, 250, 1000]}

    converted_psi = ['Coates\n1964', 'Coates & Parsons\n1966', 'Deere & Miller\n1966']

    # If called on separately will plot all the values in a bar chart type
    # If called on from the Deere-Miller plots will create the UCS Strength Criterion based on the type called
    if type == '':
        return category_names, category_values, converted_psi
    else:
        return category_names[type], category_values[type]


    ##############
    # REFERENCES #
    ##############

    # ISRM\n1977 =
    # ISRMCAT\n1979 = ISRM commission on standardization of laboratory and field tests: "Suggested methods for the quantitative description of discontinuities in rock masses" International Journal of Rock Mechanics and Mining Sciences & Geomechanics Abstracts,Volume 15, Issue 6, 1978, Pages 319-368, ISSN 0148-9062, https://doi.org/10.1016/0148-9062(78)91472-9.
    # Bieniawski\n1974 = Bieniawski ZT (1973) Engineering classification of jointed rock masses. The Civil Engineering in Southern Africa 15
    # Jennings\n1973 = Jennings JE, Brink ABA, Williams AAB (1973) Revised guide to soil profiling for civil engineering purposes in Southern Africa. The Civil Engineering in Southern Africa 15:3–12. https://doi.org/10.1016/0148-9062(74)91296-0
    # Broch & Franklin\n1972 = Broch E, Franklin JA (1972) The point-load strength test. Int. J. Rock Mech. Min. Sci. Geomech. Abstr. 9:669–676. https://doi.org/10.1016/0148-9062(72)90030-7
    # Geological Society\n1970  =
    # Deere & Miller\n1966 = DEERE, D. U. y MILLER, R. P.. Engineering Classification and Index Properties for Intact Rocks. Kirtland Air Force Base, New Mexico: 1966.
    # Coates\n1964 = Coates DF (1964) Classification of rocks for rock mechanics. International Journal of Rock Mechanics and Mining Sciences & Geomechanics Abstracts 1:421–429. https://doi.org/10.1016/0148-9062(64)90008-7
    # Coates & Parsons\n1966 = Coates DF, Parsons RC (1966) Experimental criteria for classification of rock substances. International Journal of Rock Mechanics and Mining Sciences & Geomechanics Abstracts 3:181–189. https://doi.org/10.1016/0148-9062(66)90022-2
    # ISO 14689\n2017 = ISO 14689:2017 "Geotechnical investigation and testing — Identification, description and classification of rock."
    # Anon\n1977 = Anon, Q. "The description of rock masses for engineering purposes." J Eng Geol 10 (1977): 355-388.
    # Anon\n1979 = Anon, O. H. "Classification of rocks and soils for engineering geological mapping. Part 1: rock and soil materials." .
    # Ramamurthy\n2004 = Ramamurthy, T. "A geo-engineering classification for rocks and rock masses." International Journal of Rock Mechanics and Mining Sciences 41.1 (2004): 89-101.

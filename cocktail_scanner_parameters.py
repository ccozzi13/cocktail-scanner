schema_prompt = """These are the steps you should follow:
                    1. Read an understand the JSON schema.
                    2. Read the provided recipe text and reformat it into this schema and return the JSON.
                    """

additional_prompts = """Here are additional notes to consider during your reformating:
                    1. Validate all JSON outputs to include required fields (id, name, amount, and units) and replace missing values with defaults.
                    2. Do not convert units.  Use the units in the recipe.
                    3. Replace missing or null values for amount with 1.
                    4. Replace missing or null values for units with "units".
                    5. If juice ingredients have adjectives like "fresh", "strained", "squeezed" - do not include the adjustives.  For example "fresh lime juice" should be returned as "lime juice".
                    6. If there are ingredients that have an additional recipes contained in this same text (sometimes included in Editor's Notes, or notated by 'see below'), include how to make this ingredient in the instructions field - along with the cocktail instructions.  The instructions field is one large text field, but try and format this nicely - and not completely merged with the description of the cocktail.  Perhaps separate with a string of 10 dashes.
                    7. If the sources is not a URL or web link - and it is just simple text, also add it as a tag.  Keep the other tags.  Remember to also assign it to source AND tag.
                    """

json_prompt =   """Here is the JSON schema:
                """
recipe_prompt = """Here is the recipe text: 
                """

default_model = 'gemini-2.0-flash'

bar_assistant_schema = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://barassistant.app/cocktail-01.schema.json",
    "title": "Cocktail recipe",
    "description": "Schema for a cocktail recipe including detailed ingredient data.",
    "type": "object",
    "properties": {
        "_id": {
            "description": "The unique identifier for a cocktail",
            "type": "string",
            "format": "slug",
            "minLength": 1,
            "examples": [
                "margarita"
            ]
        },
        "name": {
            "description": "Name of the recipe",
            "type": "string",
            "minLength": 1,
            "examples": [
                "Margarita"
            ]
        },
        "instructions": {
            "description": "Recipe instructions",
            "type": [
                "string",
                "null"
            ],
            "examples": [
                "Shake all ingredients with ice and strain into a chilled glass."
            ]
        },
        "created_at": {
            "description": "Date of recipe",
            "type": [
                "string",
                "null"
            ],
            "format": "date-time",
            "examples": [
                "2024-07-21T15:30:00Z"
            ]
        },
        "description": {
            "description": "Recipe description",
            "type": [
                "string",
                "null"
            ],
            "examples": [
                "A refreshing blend of tequila, lime juice, and triple sec."
            ]
        },
        "source": {
            "description": "Source of the recipe, either URL or Book referece",
            "type": [
                "string",
                "null"
            ],
            "examples": [
                "https://example.com/margarita-recipe"
            ]
        },
        "garnish": {
            "description": "Cocktail garnish",
            "type": [
                "string",
                "null"
            ],
            "examples": [
                "Lime wheel"
            ]
        },
        "abv": {
            "description": "Total ABV of made cocktail",
            "type": [
                "number",
                "null"
            ],
            "minimum": 0,
            "examples": [
                12.5
            ]
        },
        "tags": {
            "description": "Short keywords to describe cocktail",
            "type": "array",
            "uniqueItems": true,
            "items": {
                "type": "string"
            },
            "examples": [
                [
                    "refreshing",
                    "citrus",
                    "classic"
                ]
            ]
        },
        "glass": {
            "description": "Glass type",
            "type": [
                "string",
                "null"
            ],
            "examples": [
                "Coupe"
            ]
        },
        "method": {
            "description": "Cocktail method",
            "type": [
                "string",
                "null"
            ],
            "examples": [
                "Shake"
            ]
        },
        "utensils": {
            "description": "Required utensils",
            "type": "array",
            "uniqueItems": true,
            "items": {
                "type": "string"
            },
            "examples": [
                [
                    "Shaker",
                    "Strainer"
                ]
            ]
        },
        "images": {
            "description": "List of cocktail images",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "examples": [
                            "https://example.com/image.jpg",
                            "/path/to/image.png"
                        ]
                    },
                    "sort": {
                        "description": "Control the representation of the image",
                        "type": "number",
                        "minimum": 0
                    },
                    "placeholder_hash": {
                        "description": "Computed placeholder hash, like thumbhash, blurhash and similar",
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "copyright": {
                        "description": "Image copyright information",
                        "type": "string",
                        "examples": [
                            "© 2024 Bar Assistant"
                        ]
                    }
                },
                "required": [
                    "source",
                    "copyright"
                ]
            }
        },
        "ingredients": {
            "description": "List of cocktail ingredients and substitutes",
            "type": "array",
            "items": {
                "type": "object",
                "title": "Cocktail ingredient",
                "properties": {
                    "_id": {
                        "description": "The unique identifier for an ingredient",
                        "type": "string",
                        "minLength": 1,
                        "examples": [
                            "tequila"
                        ]
                    },
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "examples": [
                            "Tequila"
                        ]
                    },
                    "strength": {
                        "description": "Ingredient ABV",
                        "type": "number",
                        "minimum": 0,
                        "examples": [
                            40
                        ]
                    },
                    "description": {
                        "description": "Additional ingredient information",
                        "type": [
                            "string",
                            "null"
                        ],
                        "examples": [
                            "A Mexican spirit made from the blue agave plant."
                        ]
                    },
                    "origin": {
                        "description": "Ingredient origin",
                        "type": [
                            "string",
                            "null"
                        ],
                        "examples": [
                            "Mexico"
                        ]
                    },
                    "category": {
                        "description": "Category ingredient belongs to",
                        "type": [
                            "string",
                            "null"
                        ],
                        "examples": [
                            "Spirit"
                        ]
                    },
                    "amount": {
                        "description": "Amount of the ingredient",
                        "type": "number",
                        "minimum": 0,
                        "maximum": 99999,
                        "examples": [
                            50
                        ]
                    },
                    "units": {
                        "description": "Units for the amount",
                        "type": "string",
                        "minLength": 1,
                        "examples": [
                            "ml"
                        ]
                    },
                    "optional": {
                        "description": "Indicates if the ingredient is optional",
                        "type": "boolean",
                        "examples": [
                            false
                        ]
                    },
                    "amount_max": {
                        "description": "Maximum amount of the ingredient",
                        "type": [
                            "number",
                            "null"
                        ],
                        "minimum": 0,
                        "maximum": 99999,
                        "examples": [
                            60
                        ]
                    },
                    "note": {
                        "description": "Additional note related to the cocktail ingredient",
                        "type": [
                            "string",
                            "null"
                        ],
                        "examples": [
                            "Preferebly blanco"
                        ]
                    },
                    "substitutes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "_id": {
                                    "description": "The unique identifier for a ingredient",
                                    "type": "string",
                                    "minLength": 1,
                                    "examples": [
                                        "mezcal"
                                    ]
                                },
                                "name": {
                                    "type": "string",
                                    "minLength": 1,
                                    "examples": [
                                        "Mezcal"
                                    ]
                                },
                                "strength": {
                                    "description": "Substitute ingredient ABV",
                                    "type": "number",
                                    "minimum": 0,
                                    "examples": [
                                        40
                                    ]
                                },
                                "description": {
                                    "description": "Additional information about the substitute ingredient",
                                    "type": [
                                        "string",
                                        "null"
                                    ],
                                    "examples": [
                                        "A smoky Mexican spirit made from various types of agave."
                                    ]
                                },
                                "origin": {
                                    "description": "Substitute ingredient origin",
                                    "type": [
                                        "string",
                                        "null"
                                    ],
                                    "examples": [
                                        "Mexico"
                                    ]
                                },
                                "category": {
                                    "description": "Category the substitute ingredient belongs to",
                                    "type": [
                                        "string",
                                        "null"
                                    ],
                                    "examples": [
                                        "Spirit"
                                    ]
                                },
                                "amount": {
                                    "description": "Amount of the substitute ingredient",
                                    "type": [
                                        "number",
                                        "null"
                                    ],
                                    "examples": [
                                        50
                                    ]
                                },
                                "units": {
                                    "description": "Units for the amount",
                                    "type": [
                                        "string",
                                        "null"
                                    ],
                                    "examples": [
                                        "ml"
                                    ]
                                },
                                "amount_max": {
                                    "description": "Maximum amount of the substitute ingredient",
                                    "type": [
                                        "number",
                                        "null"
                                    ],
                                    "examples": [
                                        60
                                    ]
                                }
                            }
                        }
                    },
                    "sort": {
                        "description": "Sort order for the ingredient",
                        "type": "number",
                        "minimum": 0
                    }
                },
                "required": [
                    "_id",
                    "name",
                    "amount",
                    "units"
                ]
            }
        }
    },
    "required": [
        "_id",
        "name",
        "instructions"
    ]
}
"""

sample_recipe = """

Bar Valentina’s Espresso Martini This recipe tied for first in our Espresso Martini tasting. It calls for vanilla-infused vodka, Kahlúa, fresh espresso and rich Demerara syrup. As with real espresso, a citrus note on the palate gives the cocktail, from Bar Valentina in New York, a pleasant bitterness. “It finishes like when you bite into a chocolate-covered espresso bean,” said Izzy Tulloch, a bartender who was one of the assembled judges.

    Print
    Save

Ingredients

Serving: 1

    1 1/2 ounces vanilla bean vodka (see Editor’s Note)
    3/4 ounce espresso
    1/2 ounce coffee liqueur, preferably Kahlúa
    1/4 ounce rich Demerara syrup (2:1, sugar to water)

Garnish: 3 espresso beans
Directions

    Add all ingredients to a cocktail shaker with ice and shake vigorously.
    Double-strain into a Martini or cocktail glass.
    Garnish with 3 espresso beans in the center of the foam.

Editor's Note

Vanilla Bean Vodka
Infuse 1 liter of vodka with 2 Tahitian vanilla beans split down the middle for 24 hours. Strain out the vanilla and bottle.

"""
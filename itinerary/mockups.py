class MockUps:
    openai_response = {
        "country": "France",
        "itinerary": [
            {
                "city": "Paris",
                "latitude": "48.866667",
                "longitude": "2.333333",
                "duration": 2,
                "todo": [
                    {
                        "name": "Eiffel Tower",
                        "longitude": "2.2945",
                        "latitude": "48.8584",
                        "category": "Monument"
                    },
                    {
                        "name": "Louvre Museum",
                        "longitude": "2.3387",
                        "latitude": "48.8606",
                        "category": "Monument"
                    },
                    {
                        "name": "Le Petit Cler",
                        "longitude": "2.3387",
                        "latitude": "48.8617",
                        "category": "Gastronomy"
                    },
                    {
                        "name": "Jardin des Tuileries",
                        "longitude": "2.3317",
                        "latitude": "48.8637",
                        "category": "Nature"
                    }
                ]
            },
            {
                "city": "Nice",
                "latitude": "43.700000.",
                "longitude": "7.250000",
                "duration": 2,
                "todo": [
                    {
                        "name": "Promenade des Anglais",
                        "longitude": "7.2662",
                        "latitude": "43.6961",
                        "category": "Discovering"
                    },
                    {
                        "name": "Vieux Nice",
                        "longitude": "7.2710",
                        "latitude": "43.6984",
                        "category": "Discovering"
                    },
                    {
                        "name": "Chez Pipo",
                        "longitude": "7.2710",
                        "latitude": "43.6984",
                        "category": "Gastronomy"
                    },
                    {
                        "name": "Parc Phoenix",
                        "longitude": "7.2662",
                        "latitude": "43.6961",
                        "category": "Nature"
                    }
                ]
            },
            {
                "city": "Paris",
                "latitude": "48.866667",
                "longitude": "2.333333",
                "duration": 2,
                "todo": [
                    {
                        "name": "Notre Dame Cathedral",
                        "longitude": "2.3470",
                        "latitude": "48.8530",
                        "category": "Monument"
                    },
                    {
                        "name": "Arc de Triomphe",
                        "longitude": "2.2950",
                        "latitude": "48.8738",
                        "category": "Monument"
                    },
                    {
                        "name": "Le Petit Cler",
                        "longitude": "2.3387",
                        "latitude": "48.8617",
                        "category": "Gastronomy"
                    },
                    {
                        "name": "Jardin des Tuileries",
                        "longitude": "2.3317",
                        "latitude": "48.8637",
                        "category": "Nature"
                    }
                ]
            }
        ]
    }

    response = {
        "country": "France",
        "itinerary": [
            {
                "city": "Paris",
                "latitude": "48.866667",
                "longitude": "2.333333",
                "duration": 2,
                "todo": [
                    {
                        "name": "Eiffel Tower",
                        "longitude": "2.2945",
                        "latitude": "48.8584",
                        "category": "Monument"
                    },
                    {
                        "name": "Louvre Museum",
                        "longitude": "2.3387",
                        "latitude": "48.8606",
                        "category": "Monument"
                    },
                    {
                        "name": "Le Petit Cler",
                        "longitude": "2.3387",
                        "latitude": "48.8617",
                        "category": "Gastronomy"
                    },
                    {
                        "name": "Jardin des Tuileries",
                        "longitude": "2.3317",
                        "latitude": "48.8637",
                        "category": "Nature"
                    }
                ]
            },
            {
                "city": "Nice",
                "latitude": "43.700000.",
                "longitude": "7.250000",
                "duration": 2,
                "todo": [
                    {
                        "name": "Promenade des Anglais",
                        "longitude": "7.2662",
                        "latitude": "43.6961",
                        "category": "Discovering"
                    },
                    {
                        "name": "Vieux Nice",
                        "longitude": "7.2710",
                        "latitude": "43.6984",
                        "category": "Discovering"
                    },
                    {
                        "name": "Chez Pipo",
                        "longitude": "7.2710",
                        "latitude": "43.6984",
                        "category": "Gastronomy"
                    },
                    {
                        "name": "Parc Phoenix",
                        "longitude": "7.2662",
                        "latitude": "43.6961",
                        "category": "Nature"
                    }
                ]
            },
            {
                "city": "Paris",
                "latitude": "48.866667",
                "longitude": "2.333333",
                "duration": 2,
                "todo": [
                    {
                        "name": "Notre Dame Cathedral",
                        "longitude": "2.3470",
                        "latitude": "48.8530",
                        "category": "Monument"
                    },
                    {
                        "name": "Arc de Triomphe",
                        "longitude": "2.2950",
                        "latitude": "48.8738",
                        "category": "Monument"
                    },
                    {
                        "name": "Le Petit Cler",
                        "longitude": "2.3387",
                        "latitude": "48.8617",
                        "category": "Gastronomy"
                    },
                    {
                        "name": "Jardin des Tuileries",
                        "longitude": "2.3317",
                        "latitude": "48.8637",
                        "category": "Nature"
                    }
                ]
            }
        ]
    }

    empty_itineraries_response = {
        "code": 200,
        "result": "success",
        "message": "",
        "data": []
    }

    itineraries_response = {
        "code": 200,
        "result": "success",
        "message": "",
        "data": [
            {
                "id": 333,
                "title": "France",
                "country": "France",
                "starting_city": "Paris",
                "ending_city": "Paris",
                "start_date": "2023-12-20",
                "end_date": "2023-12-27",
                "types": None,
                "interests": None,
                "steps": None,
                "multiple_cities": False,
                "level": None,
                "user": {
                    'id': 1,
                    'display_name': "Axel Pion",
                    'email': "test.case@gmail.com"
                }
            }
        ]
    }

    itinerary_response = {
        "code": 200,
        "result": "success",
        "message": "",
        "data": {
            "id": 333,
            "title": "France",
            "country": "France",
            "starting_city": "Paris",
            "ending_city": "Paris",
            "start_date": "2023-12-20",
            "end_date": "2023-12-27",
            "types": None,
            "interests": None,
            "steps": None,
            "multiple_cities": False,
            "level": None,
            "user": {
                'id': 1,
                'display_name': "Axel Pion",
                'email': "test.case@gmail.com"
            },
            "response": {
                "country": "France",
                "itinerary": [
                    {
                        "city": "Paris",
                        "latitude": "48.866667",
                        "longitude": "2.333333",
                        "duration": 2,
                        "todo": [
                            {
                                "name": "Eiffel Tower",
                                "longitude": "2.2945",
                                "latitude": "48.8584",
                                "category": "Monument"
                            },
                            {
                                "name": "Louvre Museum",
                                "longitude": "2.3387",
                                "latitude": "48.8606",
                                "category": "Monument"
                            },
                            {
                                "name": "Le Petit Cler",
                                "longitude": "2.3387",
                                "latitude": "48.8617",
                                "category": "Gastronomy"
                            },
                            {
                                "name": "Jardin des Tuileries",
                                "longitude": "2.3317",
                                "latitude": "48.8637",
                                "category": "Nature"
                            }
                        ]
                    },
                    {
                        "city": "Nice",
                        "latitude": "43.700000.",
                        "longitude": "7.250000",
                        "duration": 2,
                        "todo": [
                            {
                                "name": "Promenade des Anglais",
                                "longitude": "7.2662",
                                "latitude": "43.6961",
                                "category": "Discovering"
                            },
                            {
                                "name": "Vieux Nice",
                                "longitude": "7.2710",
                                "latitude": "43.6984",
                                "category": "Discovering"
                            },
                            {
                                "name": "Chez Pipo",
                                "longitude": "7.2710",
                                "latitude": "43.6984",
                                "category": "Gastronomy"
                            },
                            {
                                "name": "Parc Phoenix",
                                "longitude": "7.2662",
                                "latitude": "43.6961",
                                "category": "Nature"
                            }
                        ]
                    },
                    {
                        "city": "Paris",
                        "latitude": "48.866667",
                        "longitude": "2.333333",
                        "duration": 2,
                        "todo": [
                            {
                                "name": "Notre Dame Cathedral",
                                "longitude": "2.3470",
                                "latitude": "48.8530",
                                "category": "Monument"
                            },
                            {
                                "name": "Arc de Triomphe",
                                "longitude": "2.2950",
                                "latitude": "48.8738",
                                "category": "Monument"
                            },
                            {
                                "name": "Le Petit Cler",
                                "longitude": "2.3387",
                                "latitude": "48.8617",
                                "category": "Gastronomy"
                            },
                            {
                                "name": "Jardin des Tuileries",
                                "longitude": "2.3317",
                                "latitude": "48.8637",
                                "category": "Nature"
                            }
                        ]
                    }
                ]
            }
        }
    }

    wrong_interests_response = {
        "code": 500,
        "result": "error",
        "message": "Invalid form.",
        "data": {
            'interest': ['Select a valid choice. That choice is not one of the available choices.']
        }
    }

    wrong_types_response = {
        "code": 500,
        "result": "error",
        "message": "Invalid form.",
        "data": {
            'interest': ['Select a valid choice. That choice is not one of the available choices.']
        }
    }

    itinerary_not_found_response = {
        "code": 404,
        "result": "error",
        "message": "Itinerary not found.",
        "data": []
    }

    bad_method_on_get_response = {
        "code": 400,
        "result": "error",
        "message": "Must be a GET method.",
        "data": []
    }

    bad_method_on_post_response = {
        "code": 400,
        "result": "error",
        "message": "Must be a POST method.",
        "data": []
    }

    bad_method_on_patch_response = {
        "code": 400,
        "result": "error",
        "message": "Must be a PATCH method.",
        "data": []
    }

    create_itinerary_payload = {
        "country": "France",
        "starting_city": "Paris",
        "ending_city": "Paris",
        "start_date": "2023-10-16",
        "end_date": "2023-10-22",
        "types": [1],
        "level": 1,
        "multiple_cities": True,
        "steps": [
            {
                "city": "Toulouse",
                "duration": 2
            },
            {
                "city": "Nice",
                "duration": 2
            }
        ],
        "interests": [1, 2],
        "user": 1
    }

    create_itinerary_response = {
        "code": 201,
        "result": "success",
        "message": "Itinerary created successfully.",
        "data": {
            "country": "France",
            "itinerary": [
                {
                    "city": "Paris",
                    "latitude": "48.866667",
                    "longitude": "2.333333",
                    "duration": 2,
                    "todo": [
                        {
                            "name": "Eiffel Tower",
                            "longitude": "2.2945",
                            "latitude": "48.8584",
                            "category": "Monument"
                        },
                        {
                            "name": "Louvre Museum",
                            "longitude": "2.3387",
                            "latitude": "48.8606",
                            "category": "Monument"
                        },
                        {
                            "name": "Le Petit Cler",
                            "longitude": "2.3387",
                            "latitude": "48.8617",
                            "category": "Gastronomy"
                        },
                        {
                            "name": "Jardin des Tuileries",
                            "longitude": "2.3317",
                            "latitude": "48.8637",
                            "category": "Nature"
                        }
                    ]
                },
                {
                    "city": "Nice",
                    "latitude": "43.700000.",
                    "longitude": "7.250000",
                    "duration": 2,
                    "todo": [
                        {
                            "name": "Promenade des Anglais",
                            "longitude": "7.2662",
                            "latitude": "43.6961",
                            "category": "Discovering"
                        },
                        {
                            "name": "Vieux Nice",
                            "longitude": "7.2710",
                            "latitude": "43.6984",
                            "category": "Discovering"
                        },
                        {
                            "name": "Chez Pipo",
                            "longitude": "7.2710",
                            "latitude": "43.6984",
                            "category": "Gastronomy"
                        },
                        {
                            "name": "Parc Phoenix",
                            "longitude": "7.2662",
                            "latitude": "43.6961",
                            "category": "Nature"
                        }
                    ]
                },
                {
                    "city": "Paris",
                    "latitude": "48.866667",
                    "longitude": "2.333333",
                    "duration": 2,
                    "todo": [
                        {
                            "name": "Notre Dame Cathedral",
                            "longitude": "2.3470",
                            "latitude": "48.8530",
                            "category": "Monument"
                        },
                        {
                            "name": "Arc de Triomphe",
                            "longitude": "2.2950",
                            "latitude": "48.8738",
                            "category": "Monument"
                        },
                        {
                            "name": "Le Petit Cler",
                            "longitude": "2.3387",
                            "latitude": "48.8617",
                            "category": "Gastronomy"
                        },
                        {
                            "name": "Jardin des Tuileries",
                            "longitude": "2.3317",
                            "latitude": "48.8637",
                            "category": "Nature"
                        }
                    ]
                }
            ]
        }
    }

    create_itinerary_without_payload_response = {
        "code": 400,
        "result": "error",
        "message": "Require a payload.",
        "data": []
    }

    create_itinerary_bad_payload = {
        "country": "France",
        "ending_city": "Paris",
        "start_date": "2023-10-16",
        "end_date": "2023-10-22",
        "types": [2],
        "level": 1,
        "multiple_cities": True,
        "steps": [
            {
                "city": "Toulouse",
                "duration": 2
            },
            {
                "city": "Nice",
                "duration": 2
            }
        ],
        "interests": [1, 2, 3, 4],
        "user": 1
    }

    create_itinerary_bad_payload_response = {
        "code": 500,
        "result": "error",
        "message": "Invalid form.",
        "data": {
            "starting_city": [
                "This field is required."
            ]
        }
    }

    create_itinerary_without_types_payload = {
        "country": "France",
        "starting_city": "Paris",
        "ending_city": "Paris",
        "start_date": "2023-10-16",
        "end_date": "2023-10-22",
        "level": 1,
        "multiple_cities": True,
        "steps": [
            {
                "city": "Toulouse",
                "duration": 2
            },
            {
                "city": "Nice",
                "duration": 2
            }
        ],
        "interests": [1, 2],
        "user": 1
    }

    create_itinerary_without_types_response = {
        "code": 400,
        "result": "error",
        "message": "Body must possess types.",
        "data": []
    }

    create_itinerary_without_interests_payload = {
        "country": "France",
        "starting_city": "Paris",
        "ending_city": "Paris",
        "start_date": "2023-10-16",
        "end_date": "2023-10-22",
        "types": [1],
        "level": 1,
        "multiple_cities": True,
        "steps": [
            {
                "city": "Toulouse",
                "duration": 2
            },
            {
                "city": "Nice",
                "duration": 2
            }
        ],
        "user": 1
    }

    create_itinerary_without_interests_response = {
        "code": 400,
        "result": "error",
        "message": "Body must possess interests.",
        "data": []
    }

    create_itinerary_bad_delta_payload = {
        "country": "France",
        "starting_city": "Paris",
        "ending_city": "Paris",
        "start_date": "2023-10-20",
        "end_date": "2023-10-16",
        "types": [2],
        "level": 1,
        "multiple_cities": True,
        "steps": [
            {
                "city": "Toulouse",
                "duration": 2
            },
            {
                "city": "Nice",
                "duration": 2
            }
        ],
        "interests": [1, 2],
        "user": 1
    }

    create_itinerary_bad_delta_response = {
        "code": 405,
        "result": "error",
        "message": "The delta between start date and end date can not be negative.",
        "data": {
            "start": "2023-10-20",
            "end": "2023-10-16"
        }
    }

    update_itinerary_title_payload = {
        "title": "TestUpdateTitle"
    }

    update_itinerary_title_response = {
        "code": 200,
        "result": "success",
        "message": "Title updated successfully.",
        "data": [
            {
                "id": 333,
                "title": "TestUpdateTitle",
                "country": "France",
                "starting_city": "Paris",
                "ending_city": "Paris",
                "start_date": "2023-12-20",
                "end_date": "2023-12-27",
                "types": None,
                "interests": None,
                "steps": None,
                "multiple_cities": False,
                "level": None,
                "user": {
                    'id': 1,
                    'display_name': "Axel Pion",
                    'email': "test.case@gmail.com"
                }
            }
        ]
    }

    update_itinerary_title_as_int_type_payload = {
        "title": 123
    }

    update_itinerary_title_as_int_type_response = {
        "code": 200,
        "result": "success",
        "message": "Title updated successfully.",
        "data": [
            {
                "id": 333,
                "title": "123",
                "country": "France",
                "starting_city": "Paris",
                "ending_city": "Paris",
                "start_date": "2023-12-20",
                "end_date": "2023-12-27",
                "types": None,
                "interests": None,
                "steps": None,
                "multiple_cities": False,
                "level": None,
                "user": {
                    'id': 1,
                    'display_name': "Axel Pion",
                    'email': "test.case@gmail.com"
                }
            }
        ]
    }

    update_itinerary_steps_payload = {
        "id": 333,
        "response":
        {
            "country": "France",
            "itinerary": [
                {
                    "city": "Paris",
                    "latitude": "48.866667",
                    "longitude": "2.333333",
                    "duration": 2,
                    "todo": [
                        {
                            "name": "Eiffel Tower",
                            "longitude": "2.2945",
                            "latitude": "48.8584",
                            "category": "Monument"
                        },
                        {
                            "name": "Louvre Museum",
                            "longitude": "2.3387",
                            "latitude": "48.8606",
                            "category": "Monument"
                        },
                        {
                            "name": "Le Petit Cler",
                            "longitude": "2.3387",
                            "latitude": "48.8617",
                            "category": "Gastronomy"
                        },
                        {
                            "name": "Jardin des Tuileries",
                            "longitude": "2.3317",
                            "latitude": "48.8637",
                            "category": "Nature"
                        }
                    ]
                },
                {
                    "city": "Nice",
                    "latitude": "43.700000.",
                    "longitude": "7.250000",
                    "duration": 2,
                    "todo": [
                        {
                            "name": "Promenade des Anglais",
                            "longitude": "7.2662",
                            "latitude": "43.6961",
                            "category": "Discovering"
                        },
                        {
                            "name": "Vieux Nice",
                            "longitude": "7.2710",
                            "latitude": "43.6984",
                            "category": "Discovering"
                        },
                        {
                            "name": "Chez Pipo",
                            "longitude": "7.2710",
                            "latitude": "43.6984",
                            "category": "Gastronomy"
                        },
                        {
                            "name": "Parc Phoenix",
                            "longitude": "7.2662",
                            "latitude": "43.6961",
                            "category": "Nature"
                        }
                    ]
                },
                {
                    "city": "Paris",
                    "latitude": "48.866667",
                    "longitude": "2.333333",
                    "duration": 2,
                    "todo": [
                        {
                            "name": "Notre Dame Cathedral",
                            "longitude": "2.3470",
                            "latitude": "48.8530",
                            "category": "Monument"
                        },
                        {
                            "name": "Arc de Triomphe",
                            "longitude": "2.2950",
                            "latitude": "48.8738",
                            "category": "Monument"
                        },
                        {
                            "name": "Le Petit Cler",
                            "longitude": "2.3387",
                            "latitude": "48.8617",
                            "category": "Gastronomy"
                        },
                        {
                            "name": "Jardin des Tuileries",
                            "longitude": "2.3317",
                            "latitude": "48.8637",
                            "category": "Nature"
                        }
                    ]
                }
            ]
        }
    }

    update_itinerary_steps_response = {
        "code": 200,
        "result": "success",
        "message": "JSON updated successfully.",
        "data": {
            "id": 333,
            "title": "France",
            "country": "France",
            "starting_city": "Paris",
            "ending_city": "Paris",
            "start_date": "2023-12-20",
            "end_date": "2023-12-27",
            "types": None,
            "interests": None,
            "steps": None,
            "multiple_cities": False,
            "level": None,
            "user": {
                'id': 1,
                'display_name': "Axel Pion",
                'email': "test.case@gmail.com"
            },
            "response": {
                "country": "France",
                "itinerary": [
                    {
                        "city": "Paris",
                        "latitude": "48.866667",
                        "longitude": "2.333333",
                        "duration": 2,
                        "todo": [
                            {
                                "name": "Eiffel Tower",
                                "longitude": "2.2945",
                                "latitude": "48.8584",
                                "category": "Monument"
                            },
                            {
                                "name": "Louvre Museum",
                                "longitude": "2.3387",
                                "latitude": "48.8606",
                                "category": "Monument"
                            },
                            {
                                "name": "Le Petit Cler",
                                "longitude": "2.3387",
                                "latitude": "48.8617",
                                "category": "Gastronomy"
                            },
                            {
                                "name": "Jardin des Tuileries",
                                "longitude": "2.3317",
                                "latitude": "48.8637",
                                "category": "Nature"
                            }
                        ]
                    },
                    {
                        "city": "Nice",
                        "latitude": "43.700000.",
                        "longitude": "7.250000",
                        "duration": 2,
                        "todo": [
                            {
                                "name": "Promenade des Anglais",
                                "longitude": "7.2662",
                                "latitude": "43.6961",
                                "category": "Discovering"
                            },
                            {
                                "name": "Vieux Nice",
                                "longitude": "7.2710",
                                "latitude": "43.6984",
                                "category": "Discovering"
                            },
                            {
                                "name": "Chez Pipo",
                                "longitude": "7.2710",
                                "latitude": "43.6984",
                                "category": "Gastronomy"
                            },
                            {
                                "name": "Parc Phoenix",
                                "longitude": "7.2662",
                                "latitude": "43.6961",
                                "category": "Nature"
                            }
                        ]
                    },
                    {
                        "city": "Paris",
                        "latitude": "48.866667",
                        "longitude": "2.333333",
                        "duration": 2,
                        "todo": [
                            {
                                "name": "Notre Dame Cathedral",
                                "longitude": "2.3470",
                                "latitude": "48.8530",
                                "category": "Monument"
                            },
                            {
                                "name": "Arc de Triomphe",
                                "longitude": "2.2950",
                                "latitude": "48.8738",
                                "category": "Monument"
                            },
                            {
                                "name": "Le Petit Cler",
                                "longitude": "2.3387",
                                "latitude": "48.8617",
                                "category": "Gastronomy"
                            },
                            {
                                "name": "Jardin des Tuileries",
                                "longitude": "2.3317",
                                "latitude": "48.8637",
                                "category": "Nature"
                            }
                        ]
                    }
                ]
            }
        }
    }

    update_itinerary_steps_on_itinerary_not_found_payload = {
        "id": 777,
        "response":
        {
            "country": "France",
            "itinerary": [
                {
                    "city": "Paris",
                    "latitude": "48.866667",
                    "longitude": "2.333333",
                    "duration": 2,
                    "todo": [
                        {
                            "name": "Eiffel Tower",
                            "longitude": "2.2945",
                            "latitude": "48.8584",
                            "category": "Monument"
                        },
                        {
                            "name": "Louvre Museum",
                            "longitude": "2.3387",
                            "latitude": "48.8606",
                            "category": "Monument"
                        },
                        {
                            "name": "Le Petit Cler",
                            "longitude": "2.3387",
                            "latitude": "48.8617",
                            "category": "Gastronomy"
                        },
                        {
                            "name": "Jardin des Tuileries",
                            "longitude": "2.3317",
                            "latitude": "48.8637",
                            "category": "Nature"
                        }
                    ]
                },
                {
                    "city": "Nice",
                    "latitude": "43.700000.",
                    "longitude": "7.250000",
                    "duration": 2,
                    "todo": [
                        {
                            "name": "Promenade des Anglais",
                            "longitude": "7.2662",
                            "latitude": "43.6961",
                            "category": "Discovering"
                        },
                        {
                            "name": "Vieux Nice",
                            "longitude": "7.2710",
                            "latitude": "43.6984",
                            "category": "Discovering"
                        },
                        {
                            "name": "Chez Pipo",
                            "longitude": "7.2710",
                            "latitude": "43.6984",
                            "category": "Gastronomy"
                        },
                        {
                            "name": "Parc Phoenix",
                            "longitude": "7.2662",
                            "latitude": "43.6961",
                            "category": "Nature"
                        }
                    ]
                },
                {
                    "city": "Paris",
                    "latitude": "48.866667",
                    "longitude": "2.333333",
                    "duration": 2,
                    "todo": [
                        {
                            "name": "Notre Dame Cathedral",
                            "longitude": "2.3470",
                            "latitude": "48.8530",
                            "category": "Monument"
                        },
                        {
                            "name": "Arc de Triomphe",
                            "longitude": "2.2950",
                            "latitude": "48.8738",
                            "category": "Monument"
                        },
                        {
                            "name": "Le Petit Cler",
                            "longitude": "2.3387",
                            "latitude": "48.8617",
                            "category": "Gastronomy"
                        },
                        {
                            "name": "Jardin des Tuileries",
                            "longitude": "2.3317",
                            "latitude": "48.8637",
                            "category": "Nature"
                        }
                    ]
                }
            ]
        }
    }

import typing

def greet(name: str, last_name):
    # method suggestions from the IDE come from the type hinting
    greeting = f"Hello, {name.capitalize()} {last_name.capitalize()}"  
    return greeting

def greet_age(name: str, age: int):
    # mypy will indicate this is a problem
    greeting = f"Hello {name.capitalize()}, your age is " + age
    return greeting

def dict_params(my_dict: typing.Dict[str, int]):
    for k, v in my_dict.items():
        print(k.capitalize())
        print(v.as_integer_ratio())
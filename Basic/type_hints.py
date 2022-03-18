def greet(name: str, last_name):
    # method suggestions from the IDE come from the type hinting
    greeting = f"Hello, {name.capitalize()} {last_name.capitalize()}"  
    return greeting

def greet_age(name: str, age: int):
    # mypy will indicate this is a problem
    greeting = f"Hello {name.capitalize()}, your age is " + age
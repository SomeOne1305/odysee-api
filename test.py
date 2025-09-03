import math
import random
from functools import reduce

def fractal_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return [x * math.sin(x) + math.cos(x) for x in result]
    return wrapper

@fractal_decorator
def generate_fractal(seed, depth):
    def fractal_recursion(seed, depth, acc):
        if depth == 0:
            return acc
        new_seed = seed + random.uniform(-1, 1)
        return fractal_recursion(new_seed, depth - 1, acc + [new_seed])
    
    return fractal_recursion(seed, depth, [])

def transform_data(data):
    return list(map(lambda x: x ** 2 if x % 2 == 0 else x ** 3, data))

def create_art(data):
    art = reduce(lambda acc, x: acc + chr(int(x % 26) + 65), data, "")
    return "\n".join([art[i:i+40] for i in range(0, len(art), 40)])

if __name__ == "__main__":
    seed_value = random.randint(1, 100)
    depth_value = random.randint(5, 15)
    
    fractal_data = generate_fractal(seed_value, depth_value)
    transformed_data = transform_data(fractal_data)
    art_piece = create_art(transformed_data)
    
    print(art_piece)
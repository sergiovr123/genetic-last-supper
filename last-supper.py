import numpy as np
import requests
from PIL import Image, ImageDraw
import io

def fetch_image(url):
    """ Función para cargar una imagen desde una URL. """
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content)).convert('RGBA')
    return image

def generate_individual(image_size, num_triangles=200):  # Aumentar el número de triángulos
    """ Generar un individuo con triángulos aleatorios. """
    image = Image.new('RGBA', image_size)
    draw = ImageDraw.Draw(image)
    for _ in range(num_triangles):
        polygon = [(np.random.randint(0, image_size[0]), np.random.randint(0, image_size[1])) for _ in range(3)]
        color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(50, 256))
        draw.polygon(polygon, fill=color)
    return image

def compute_fitness(individual, reference):
    """ Calcular la diferencia entre dos imágenes. """
    individual_array = np.array(individual)
    reference_array = np.array(reference)
    return np.sum(np.square(individual_array - reference_array))

def crossover(parent1, parent2):
    """ Sistema muy básico de cruce de dos individuos. """
    mask = np.random.randint(0,2,size=parent1.size)  # Máscara de cruce binaria
    new_data = np.where(mask, parent1.tobytes(), parent2.tobytes())
    new_image = Image.frombytes('RGBA', parent1.size, new_data)
    return new_image

def mutate(individual, mutation_rate=0.1):  # Aumentar la tasa de mutación para más exploración
    """ Mutar un individuo cambiando algunos de sus triángulos. """
    draw = ImageDraw.Draw(individual)
    size = individual.size
    for _ in range(int(mutation_rate * 500)):  # Incrementar número de mutaciones
        polygon = [(np.random.randint(0, size[0]), np.random.randint(0, size[1])) for _ in range(3)]
        color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(100, 256))
        draw.polygon(polygon, fill=color)
    return individual

URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg/300px-The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg"
reference_image = fetch_image(URL)

# Configuración inicial
population_size = 20
num_generations = 5000
num_triangles = 200

# Iniciar población
population = [generate_individual(reference_image.size, num_triangles) for _ in range(population_size)]

# Proceso evolutivo
for generation in range(num_generations):
    sorted_population = sorted(population, key=lambda x: compute_fitness(x, reference_image))
    best_individual = sorted_population[0]
    print(f"Generación {generation}, Mejor aptitud: {compute_fitness(best_individual, reference_image)}")
    # Implementar la selección y reproducción
    # Este es un ejemplo simplificado. Desarrollar una selección y cruce más avanzados es necesario para mejores resultados.

# Mostrar el mejor individuo
best_individual.show()
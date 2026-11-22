import random


#S08 Dispensacion de alcohol en barra
def simular_alcohol():
    # Simulamos una cantidad aleatoria de bebidasque se han servido
    bebidas = random.randint(0, 10)
    return bebidas


# S09 Tabaco y tragaperras.
def simular_maquinas():
    # Simulamos el dinero que entra en las maquinas
    tabaco = random.uniform(0.0, 50.0)
    tragaperras = random.uniform(0.0, 150.0)

    total_recaudado = tabaco + tragaperras
    return round(total_recaudado, 2)


#S07 Consumo electrico
def simular_consumo_electrico(estado_bar, num_clientes):
    consumo_base = 2.5

    if estado_bar == "cerrado":
        variacion = random.uniform(0.0, 0.5)
        return round(consumo_base + variacion, 2)

    consumo_abierto = consumo_base + 3.0
    consumo_clientes = num_clientes * 0.15
    ruido = random.uniform(-0.5, 1.5)

    total = consumo_abierto + consumo_clientes + ruido
    return round(total, 2)
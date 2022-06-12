from location_graph import *


LOCATION = 'Catalão, Brazil'

PLACES = {
    "Paróquia Nossa Senhora Mãe de Deus": (-47.946938, -18.166051),
    "Morrinho de São João": (-47.942575, -18.155446),
    "Represa do Clube do Povo": (-47.930308, -18.167669),
    "Praça Duque de Caxias": (-47.948893, -18.171738),
    "Parque Santa Cruz": ( -47.926398, -18.160987),
    "Parque Municipal Calixto Abraão": (-47.937080, -18.170406),
    "Museu Cornélio Ramos": (-47.945922, -18.170016),
    "Praça Getúlio Vargas": (-47.948157, -18.168707),
    "Praça da Bíblia": (-47.962336, -18.166756),
    "Parque Linear do Corrego Monsenhor Souza": (-47.958518, -18.165690),
    "Universidade Federal de Catalão": (-47.929666, -18.154480)
}

NETWORK_TYPE = 'walk' # (string {"all_private", "all", "bike", "drive", "drive_service", "walk"})

START_PLACE = "Universidade Federal de Catalão"
END_PLACE = "Universidade Federal de Catalão"

TEST_SAMPLES = [
[10, 2, 0, 1, 9, 4, 3, 7, 5, 8, 6, 10],
[10, 0, 1, 5, 4, 8, 7, 2, 9, 6, 3, 10],
[10, 8, 0, 6, 2, 4, 9, 7, 3, 5, 1, 10],
[10, 3, 1, 4, 9, 0, 8, 2, 5, 7, 6, 10],
[10, 8, 9, 2, 0, 7, 6, 4, 1, 5, 3, 10],
[10, 4, 6, 1, 9, 8, 3, 2, 0, 7, 5, 10],
[10, 4, 6, 1, 5, 9, 8, 3, 2, 7, 0, 10],
[10, 9, 6, 3, 2, 4, 7, 5, 8, 1, 0, 10],
[10, 7, 3, 2, 1, 4, 5, 6, 0, 9, 8, 10],
[10, 4, 9, 2, 8, 3, 7, 1, 5, 0, 6, 10],
[10, 4, 5, 6, 7, 2, 9, 3, 1, 8, 0, 10],
[10, 2, 5, 9, 8, 7, 4, 0, 1, 6, 3, 10]
]



def main():

    print('Hello world!')
    lc_graph = LocationGraph(LOCATION, PLACES, NETWORK_TYPE)

    PLACES_KEYS = list(PLACES.keys())

    rt = lc_graph.newRoute(PLACES_KEYS.index(START_PLACE), PLACES_KEYS.index(END_PLACE))

    print(rt.places, rt.cost)

    model = lc_graph.travellingSalesman(PLACES_KEYS.index(START_PLACE), 'SA',
                                        num_cycles=100,
                                        num_att_per_cycles=50,
                                        init_temp=200)

    model.run(rt)

    print(model.best_route.places, model.best_route.cost)

    route_map = lc_graph.createRouteMap(model)
    route_map.save('optimal_route.html')
    
def ga_test():

    print('Hello world!')
    lc_graph = LocationGraph(LOCATION, PLACES, NETWORK_TYPE)
    
    PLACES_KEYS = list(PLACES.keys())
    
    rt_1 = lc_graph.newRoute(PLACES_KEYS.index(START_PLACE), PLACES_KEYS.index(END_PLACE), [10, 2, 3, 5, 0, 7, 4, 9, 6, 1, 8, 10])
    rt_2 = lc_graph.newRoute(PLACES_KEYS.index(START_PLACE), PLACES_KEYS.index(END_PLACE), [10, 7, 5, 3, 9, 4, 0, 1, 6, 8, 2, 10])
    
    initial_pop = []
    for i in TEST_SAMPLES:
        initial_pop.append(lc_graph.newRoute(PLACES_KEYS.index(START_PLACE), PLACES_KEYS.index(END_PLACE), i))
        
    model = lc_graph.travellingSalesman(PLACES_KEYS.index(START_PLACE), 'GA',
                                        num_generations=2000,
                                        population_size=400,
                                        mutation_prob=0.1)
                                    

    model.run()
    print(model.best_route.places, model.best_route.cost)
    
    route_map = lc_graph.createRouteMap(model)
    route_map.save('optimal_route_GA.html')


if __name__ == '__main__':

    # main()
    ga_test()


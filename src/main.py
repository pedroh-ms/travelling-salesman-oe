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


def printBestRoute(route):
    print('Best solution found:')
    print(f'Route -> {route.places}')
    print(f'Cost -> {route.cost}')    


def sa_test():

    print('Travelling salesman solved with simulated annealing...')
    lc_graph = LocationGraph(LOCATION, PLACES, NETWORK_TYPE)

    PLACES_KEYS = list(PLACES.keys())

    rt = lc_graph.newRoute(PLACES_KEYS.index(START_PLACE), PLACES_KEYS.index(END_PLACE))

    model = lc_graph.travellingSalesman(PLACES_KEYS.index(START_PLACE), 'SA',
                                        num_cycles=100,
                                        num_att_per_cycles=50,
                                        init_temp=200)

    model.run(rt)
    printBestRoute(model.best_route)

    route_map = lc_graph.createRouteMap(model)
    route_map.save('optimal_route_SA.html')
    

def ga_test():

    print('Travelling salesman solved with genetic algorithm...')
    lc_graph = LocationGraph(LOCATION, PLACES, NETWORK_TYPE)
    
    PLACES_KEYS = list(PLACES.keys())
           
    model = lc_graph.travellingSalesman(PLACES_KEYS.index(START_PLACE), 'GA',
                                        num_generations=5000,
                                        population_size=100,
                                        mutation_prob=0.1)
                                    

    model.run()
    printBestRoute(model.best_route)
    
    route_map = lc_graph.createRouteMap(model)
    route_map.save('optimal_route_GA.html')


if __name__ == '__main__':

    # sa_test()
    ga_test()


import math
import pickle
import signal
from tqdm import tqdm
from collections import Counter, defaultdict


# Register CTRL+C to stop during phase 1 if it does not converge and 
# continue with phase 2
SIGINT_catched = False

def signal_handler(sig, frame):
    global SIGINT_catched
    print('\nFinishing iteration and stopping phase 1...')
    SIGINT_catched = True

signal.signal(signal.SIGINT, signal_handler)




def louvain(G):
    """
    Given a graph G, finds the optimal community for each node following the Louvain method

    Parameters
    ----------
    G : graph
        Must be an undirected weighted graph in the form of a dictionary in the form of G[v]-->Counter structure
        which has as key the neighbors (u1,u2,..) of v, and as value the weight of the edge (integer)
        between v and the neighbor. Example: G[v][u] = weight of the edge between v,u. Note that it 
        must be enforced G[v][u] == G[u][v]. In addition, by using a Counter structure, if the edge
        between u,v does not exist, then G[u][v] == 0. Also a defaultdict(int) can do the job

    Returns
    -------
    communities : dict
        Dictionary mapping each node to a community. Example: communities[v] --> community of node v
    """

    communities,nodes_merged_into,sum_in,sum_tot,k,kin = INIT_PHASE1(G, first_init=True)
    n_iter = 0   #counter for phase1-phase2 iterations

    while True:
        n_iter += 1
        communities,cont = PHASE1(G,communities,sum_in,sum_tot,k,kin)
        if not cont:
            break
        G,communities,nodes_merged_into = PHASE2(G, communities, nodes_merged_into)
        sum_in,sum_tot,k,kin = INIT_PHASE1(G)
        print(f"# {n_iter}")
    
    return communities

        




def INIT_PHASE1(G, first_init=False):
    if first_init:
        communities = {}
        nodes_merged_into = defaultdict(list)
    sum_in = {}               # Sum of weights of edges Inside the community
    sum_tot = Counter()       # Sum of weights of edges incident to nodes in C
    k = {}                    # Sum of weights of edges incident to i
    kin = {}
    for v in G:
        if first_init:
            communities[v] = v
        sum_in[v] = 0
        k[v] = 0
        kin[v] = Counter()
        for w in G[v]:
            k[v]+= G[v][w]
            sum_tot[v]+= G[v][w]
            kin[v][w] = G[v][w]

    if first_init:
        return communities,nodes_merged_into,sum_in,sum_tot,k,kin
    return sum_in,sum_tot,k,kin 




def PHASE1(G,communities,sum_in,sum_tot,k,kin,):
    updated = True
    for_counter = 0

    m = 0
    for v in G:
        for w in G[v]:
            if v < w:
                m+=G[v][w]

    global SIGINT_catched
    SIGINT_catched = False
    while updated and not SIGINT_catched:
        updated = False
        for_counter += 1

        # stats
        n_nodes = len(G.keys())
        updates_per_iter = 0

        for i, i_neighbors in tqdm(G.items()):
            max_delta_Q = -1
            max_community = None

            for j in i_neighbors:
                C = communities[j]
                # Compute change in modularity by moving node i into
                # the community C of the neighbour j

                delta_Q = 0     # Modularity Gain  
                
                gain = (sum_in[C] + kin[i][C])/(2*m) - pow(((sum_tot[C]+k[i])/(2*m)),2)
                loss = (sum_in[C])/(2*m) - pow((sum_tot[C])/(2*m),2) - pow((k[i])/(2*m),2)

                delta_Q = gain - loss


                if delta_Q > max_delta_Q:
                    max_delta_Q = delta_Q
                    max_community = communities[j]

            if max_delta_Q > 0 and max_community!=communities[i]:
                updates_per_iter+=1
                old_community = communities[i]
                communities[i] = max_community
                updated = True

                for j in i_neighbors:
                    weight = G[i][j]

                    # update sum_in
                    if communities[j] == old_community:
                        sum_in[old_community] -= weight
                    if communities[j] == max_community:
                        sum_in[max_community] += weight

                    # update sum_tot
                    if communities[j] != old_community and communities[j] != max_community:
                        sum_tot[old_community] -= weight
                        sum_tot[max_community] += weight
                    elif communities[j] == old_community:
                        sum_tot[old_community] += weight
                        sum_tot[max_community] += weight
                    elif communities[j] == max_community:
                        sum_tot[old_community] -= weight
                        sum_tot[max_community] -= weight

                    # update kin
                    kin[j][old_community] -= weight
                    kin[j][max_community] += weight

        # stats
        ratio = updates_per_iter/n_nodes
        print(f"updates_per_iter:    {updates_per_iter}")
        print(f"update ratio    :    {ratio*100}%")


        
    # Ask to continue if SIGINT was catched
    if SIGINT_catched:
        cont = ""
        while cont != "Y" and cont != "N":
            cont = input("Phase 1 stopped, continue execution with phase 2? (Y/N) ")
        if cont == "Y":
            return communities,True
        else:
            return communities,False   
 

    # If performed more than one for-loop iteration continue with phase2, otherwise stop the algorithm
    if for_counter > 1:
        return communities,True
    else:
        return communities,False




#communities[v] --> la community di v


def PHASE2(G, communities, nodes_merged_into):
    print(" [*] Starting PHASE2")

    G_com = {}

    # Update communities of merged nodes
    print("Update communities of merged nodes")
    for node in tqdm(G):
        community = communities[node]
        #if 'node' and its community aren't the same, then the node is merged into a different node
        #I've to update all the nodes merged into 'node' to the new community
        if node != community:
            merging_node = node
            merged_nodes = nodes_merged_into[merging_node]

            # for every node already merged update its community
            for merged_node in merged_nodes:
                communities[merged_node] = community
            
            nodes_merged_into[community].extend(merged_nodes)
            del nodes_merged_into[merging_node]



    # Set community graph nodes
    for c in set(communities.values()):
        G_com[c] = Counter()

    # Set community graph edges
    print("Setting community graph edges")
    for v in tqdm(list(G)):
        cv = communities[v]
        for w in G[v]:
            cw = communities[w]
            
            if cv != cw:
                G_com[cv][cw] += 1
                G_com[cw][cv] += 1

        del G[v]

    return G_com, communities, nodes_merged_into







#   -   -   -    TEST CODE    -    -    -


#test code
G1 = {
    1: Counter({2:10, 3:10, 4:10, 5:1}),
    2: Counter({1:10, 3:10, 4:10, 6:1}),
    3: Counter({1:10, 2:10, 4:10}),
    4: Counter({1:10, 2:10, 3:10}),
    5: Counter({6:10, 7:10, 8:10, 1:1}),
    6: Counter({5:10, 7:10, 8:10, 2:1}),
    7: Counter({5:10, 6:10, 8:10}),
    8: Counter({5:10, 6:10, 7:10})
}


#other test code
G2 = {
    1:Counter({2:1, 6:1, 3:1, 4:1}),
    2:Counter({1:1}),
    3:Counter({1:1, 4:1, 5:1}),
    4:Counter({1:1, 3:1, 5:1, 7:1}),
    5:Counter({3:1, 4:1, 6:1}),
    6:Counter({1:1, 5:1, 11:1}),
    7:Counter({4:1, 8:1, 10:1, 9:1}),
    8:Counter({7:1, 9:1, 10:1}),
    9:Counter({7:1, 8:1, 10:1}),
    10:Counter({8:1, 7:1, 9:1, 12:1}),
    11:Counter({6:1, 14:1, 13:1, 12:1}),
    12:Counter({11:1, 13:1, 15:1, 10:1}),
    13:Counter({11:1, 14:1, 12:1, 15:1}),
    14:Counter({11:1, 13:1}),
    15:Counter({13:1, 12:1})
}


TESTING = False

if __name__ == '__main__':
    if TESTING:
        print("Using testing graph")
        communities = louvain(G1)
        exit()

    with open("raw\\graph-compressed_weighted_dict_1.pickle", "rb") as f:
        G = pickle.load(f)

    n_nodes = len(G.keys())
    print(f"nodes: {n_nodes}")
    n_edges = 0
    for n, neigh in G.items():
        n_edges += len(neigh)
    print(f"edges: {n_edges}")
    
    communities = louvain(G)
    n_communities = len(set(communities.values()))


    print(f"communities: {n_communities}")

    with open("raw\\communities.pickle", "wb") as f:
        pickle.dump(communities, f)



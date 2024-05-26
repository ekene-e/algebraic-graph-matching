### Algebraic algorithms for graph matching
Here we seek to implement some of the more well-known algebraic (and parameterised algebraic) algorithms for graph matching.
This is a work in progress, and we will be adding more algorithms as we go along. Until Chelsea Football Club becomes a
proper footballing institution again. Or until there are no more algebraic graph matching algorithms left in the world.
Whichever comes last. Currently we have the following algorithms implemented:
* The [Rabin-Vazirani algorithm](https://web.eecs.umich.edu/~pettie/matching/Rabin-Vazirani-randomized-maximum-matching.pdf)
    by Rabin and Vazirani (1989). This algorithm is a Monte Carlo algorithm (although it can be made into a Las Vegas algorithm
    by some smart parallelization) that finds a maximum matching in a graph in expected time $O(n^{\omega+1})$, where $n$ is
    the number of vertices in the graph. An implementation of this algorithm can be found in the `rabin_vazirani.py` file.
* The [Mucha-Sankowski algorithm](https://web.eecs.umich.edu/~pettie/matching/Mucha-Sankowski-maximum-matching-matrix-multiplication.pdf) by
    Mucha and Sankowski (2004). Here, there are really two algorithms: first, one that brings the runtime of the Rabin-Vazirani
    algorithm down to $O(n^3)$ by applying the elimination theorem from linear algebra on the inverse of the Tutte matrix of the
    graph, and second, an algorithm for bipartite graphs that brings the runtime down to $O(n^{\omega})$ by pivoting and testing
    whether an entry of the Edmonds matrix (an analogue of the Tutte matrix for bipartite graphs) is zero. An implementation of
    the first algorithm can be found in the `mucha_sankowski_general.py` file, while an implementation of the second algorithm
    can be found in the `mucha_sankowski_bipartite.py` file.
* [Harvey's algorithm](https://web.eecs.umich.edu/~pettie/matching/Harvey-maximum-matching-j-version.pdf) by Nicholas Harvey
    (2009). This algorithm finds a maximum matching in a graph in time $O(n^{\omega})$, improving upon the ideas from earlier
    work in this area by smartly choosing which areas of the Tutte matrix are worth updating first (as the matching is
    constructed, that is). An implementation of this algorithm can be found in the `harvey.py` file. Here $\omega$
    is the matrix multiplication constant.
* The [Bentert-Heeger-Koana algorithm](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2023.16) by Bentert, 
    Heeger, and Koana (2023). This algorithm is a randomised algorithm that builds upon earlier ideas from Alon and Yuster
    (2007) and Fomin et. al (2015) to form a parameterised algorithm that, given a $K$-separator of a graph, finds a maximum
    matching in the graph in expected time $O(Kn^{\omega-1})$, where $n$ is the number of vertices in the graph and $\omega$
    is the matrix multiplication constant. An implementation of this algorithm can be found in the `bentert_heeger_koana.py`
    file.

Also we have implemented the much more well-known (combinatorial) [blossom algorithm](https://en.wikipedia.org/wiki/Blossom_algorithm)
by Edmonds (1965) for finding a maximum matching in a graph. This algorithm is implemented in the `edmonds_blossom.py`
file.

A nice resource for finding many matching algorithms is the [Matching Algorithms Zoo](https://web.eecs.umich.edu/~pettie/matching/)
by Seth Pettie.
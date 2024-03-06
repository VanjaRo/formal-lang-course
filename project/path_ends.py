from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.nfa import graph_to_nfa
from project.dfa import regex_to_dfa
from project.finite_automaton import FiniteAutomaton, intersect_automata

# haven't found NodeView in networkx
def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple[NodeView, NodeView]]:
    nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    dfa = regex_to_dfa(regex)

    bin_matrix_for_graph = FiniteAutomaton(nfa)
    bin_matrix_for_query = FiniteAutomaton(dfa)

    bin_matrix_intersected = intersect_automata(
        bin_matrix_for_graph, bin_matrix_for_query
    )

    start_states = bin_matrix_intersected.get_start_states()
    final_states = bin_matrix_intersected.get_final_states()

    transitive = bin_matrix_intersected.get_transitive_closure()

    result = set()

    for first_state, second_state in zip(*transitive.nonzero()):
        if first_state in start_states and second_state in final_states:
            result.add(
                (
                    first_state // bin_matrix_for_query.number_of_states,
                    second_state // bin_matrix_for_query.number_of_states,
                )
            )

    return result

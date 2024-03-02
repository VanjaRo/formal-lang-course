from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
)
from typing import Set

from networkx import MultiDiGraph


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int] = None, final_states: Set[int] = None
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    for edge in graph.edges(data=True):
        nfa.add_transition(edge[0], edge[2]["label"], edge[1])

    if not start_states:
        start_states = graph.nodes
    if not final_states:
        final_states = graph.nodes

    for node in start_states:
        nfa.add_start_state(State(node))

    for node in final_states:
        nfa.add_final_state(State(node))

    return nfa

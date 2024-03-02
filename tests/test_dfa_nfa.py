from project.dfa import regex_to_dfa
from pyformlang.finite_automaton import Symbol, NondeterministicFiniteAutomaton, State

from project.nfa import graph_to_nfa
from networkx import MultiDiGraph
from cfpq_data import labeled_two_cycles_graph


# dfa
def test_empty_regex():
    dfa = regex_to_dfa("")
    assert dfa.is_deterministic()
    assert dfa.is_empty()


def test_asteris_regex():
    dfa = regex_to_dfa("1*")
    assert dfa.accepts([Symbol("1")])
    assert dfa.accepts([Symbol("1"), Symbol("1")])


def test_alternation_regex():
    dfa = regex_to_dfa("33|43")
    assert dfa.accepts([Symbol("33")])
    assert dfa.accepts([Symbol("43")])
    assert not dfa.accepts([Symbol("007")])


def test_space_regex():
    dfa = regex_to_dfa("42 43")
    assert dfa.accepts([Symbol("42"), Symbol("43")])
    # not concat
    assert not dfa.accepts([Symbol("4243")])


# nfa
def test_nfa_empty_graph():
    nfa = graph_to_nfa(MultiDiGraph())
    assert nfa.is_empty()


def test_nfa_two_cycles_graph():
    tw_cy_graph = labeled_two_cycles_graph(1, 1, labels=("a", "b"))
    nfa = graph_to_nfa(tw_cy_graph, {0}, {1})

    test_nfa = NondeterministicFiniteAutomaton()
    test_nfa.add_start_state(State(0))
    test_nfa.add_final_state(State(1))

    for start, finish, label in tw_cy_graph.edges(data="label"):
        test_nfa.add_transition(State(start), Symbol(label), State(finish))

    assert str(nfa.to_regex()) == str(test_nfa.to_regex())

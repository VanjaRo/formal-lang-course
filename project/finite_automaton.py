from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol, State
from scipy.sparse import dok_matrix, kron
from typing import Iterable


class FiniteAutomaton:
    # nfa is parent class for dfa,
    # so we can construct as if all incoming automatons are nfa
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.start_states = set()
            self.final_states = set()
            self.states_count = 0
            self.states_indices = {}
            self.bin_matrix = {}
        else:
            self.start_states = nfa.start_states
            self.final_states = nfa.final_states
            self.states_count = len(nfa.states)
            self.states_indices = {
                state: index for (index, state) in enumerate(nfa.states)
            }
            self.bin_matrix = self.build_bin_matrix(nfa)

    def build_bin_matrix(self, nfa: NondeterministicFiniteAutomaton):

        indexes = {state: index for index, state in enumerate(nfa.states)}
        matrix = {}
        nfa_dict = nfa.to_dict()
        for label in nfa.symbols:
            tmp_matrix = dok_matrix((self.states_count, self.states_count), dtype=bool)
            for state_from, transition in nfa_dict.items():
                target_states = set()
                if label in transition:
                    state = transition[label]
                    if isinstance(state, set):
                        target_states = state
                    else:
                        target_states = {state}

                for state_to in target_states:
                    tmp_matrix[
                        indexes[state_from],
                        indexes[state_to],
                    ] = True

            matrix[label] = tmp_matrix

        return matrix

    def build_nfa(
        self,
    ) -> NondeterministicFiniteAutomaton:

        matrix = self.bin_matrix
        indexes = self.states_indices

        nfa = NondeterministicFiniteAutomaton()

        for mark in matrix.keys():
            marked_array = matrix[mark].toarray()
            for i in range(len(marked_array)):
                for j in range(len(marked_array)):
                    if marked_array[i][j]:
                        nfa.add_transition(indexes[State(i)], mark, indexes[State(j)])

        for start_state in self.start_states:
            nfa.add_start_state(indexes[State(start_state)])
        for final_state in self.final_states:
            nfa.add_final_state(indexes[State(final_state)])

        return nfa

    def get_transitive_closure(self):
        if len(self.bin_matrix) == 0:
            return dok_matrix((0, 0), dtype=bool)

        transitive_closure = sum(self.bin_matrix.values())
        prev = transitive_closure.nnz
        curr = 0

        while prev != curr:
            transitive_closure += transitive_closure @ transitive_closure
            prev = curr
            curr = transitive_closure.nnz

        return transitive_closure

    def accepts(self, word: Iterable[Symbol]) -> bool:

        return self.build_nfa().accepts(word)

    def is_empty(self) -> bool:
        transitive_closure = self.get_transitive_closure()

        return len(transitive_closure.nonzero()) == 0

    def get_start_states(self):
        return self.start_states

    def get_final_states(self):
        return self.final_states


def intersect_automata(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:
    fa = FiniteAutomaton()
    labels = automaton1.bin_matrix.keys() & automaton2.bin_matrix.keys()

    for label in labels:
        fa.bin_matrix[label] = kron(
            automaton1.bin_matrix[label], automaton2.bin_matrix[label]
        )

    for first_state, first_index in automaton1.states_indices.items():
        for second_state, second_index in automaton2.states_indices.items():
            state_index = first_index * automaton2.states_count + second_index

            fa.states_indices[state_index] = state_index

            if (
                first_state in automaton1.start_states
                and second_state in automaton2.start_states
            ):
                fa.start_states.add(state_index)
            if (
                first_state in automaton1.final_states
                and second_state in automaton2.final_states
            ):
                fa.final_states.add(state_index)

    fa.states_count = automaton1.states_count * automaton2.states_count

    return fa

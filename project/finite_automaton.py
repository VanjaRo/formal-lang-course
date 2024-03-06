from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from scipy import sparse


class FiniteAutomaton:
    # nfa is parent class for dfa,
    # so we can construct as if all incoming automatons are nfa
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.start_states = set()
            self.final_states = set()
            self.states_count = {}
            self.states_indices = {}
            self.bin_matrix = {}
        else:
            self.start_states = nfa.start_states
            self.final_states = nfa.final_states
            self.states_count = {}
            self.states_indices = {
                state: index for (index, state) in enumerate(nfa.states)
            }
            self.bin_matrix = self.build_bin_matrix(nfa)

    def build_bin_matrix(self, nfa: NondeterministicFiniteAutomaton):
        matrix = {}
        for first_state, transition in nfa.to_dict().items():
            for label, target_states in transition.items():
                if not isinstance(target_states, set):
                    target_states = {target_states}

                for state in target_states:
                    if label not in matrix:
                        matrix[label] = sparse.dok_matrix(
                            (self.number_of_states, self.number_of_states), dtype=bool
                        )
                    f = self.states_indices.get(first_state)
                    s = self.states_indices.get(state)
                    matrix[label][f, s] = True

        return matrix

    def get_transitive_closure(self):
        if len(self.bin_matrix) == 0:
            return sparse.dok_matrix((0, 0), dtype=bool)

        transitive_closure = sum(self.bin_matrix.values())
        prev = transitive_closure.nnz
        curr = 0

        while prev != curr:
            transitive_closure += transitive_closure @ transitive_closure
            prev = curr
            curr = transitive_closure.nnz

        return transitive_closure

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
        fa.bin_matrix[label] = sparse.kron(
            automaton1.bin_matrix[label], automaton2.bin_matrix[label]
        )

    for first_state, first_index in automaton1.states_indices.items():
        for second_state, second_index in automaton2.states_indices.items():
            state_index = first_index * automaton2.number_of_states + second_index

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

    fa.number_of_states = automaton1.number_of_states * automaton2.number_of_states

    return fa

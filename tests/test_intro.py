import pytest
import project.graph as g
import filecmp
import os


def test_graph_from_csv():
    graph = g.graph_from_csv("go")
    assert graph.number_of_nodes() == 582929
    assert graph.number_of_edges() == 1437437


def test_get_graph_info():
    info = g.graph_info("go")

    assert info[0] == "go"
    assert info[1] == 582929
    assert info[2] == 1437437
    assert len(info[3]) == 1437437

    assert info[3][3] == "hasRelatedSynonym"


def test_make_two_cycle_graph_test():
    graph = g.make_two_cycle_graph(2, 2, ("1", "2"))
    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 6


def test_save_graph_dot():
    graph = g.make_two_cycle_graph(2, 2, ("0", "1"))
    g.save_graph_dot("tests/test_graphs/new_two_cycle1.dot", graph)

    assert filecmp.cmp(
        "tests/test_graphs/new_two_cycle1.dot",
        "tests/test_graphs/expected_two_cycle1.dot",
        shallow=False,
    )

    os.remove("tests/test_graphs/new_two_cycle1.dot")


if __name__ == "__main__":
    test_save_graph_dot()

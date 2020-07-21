import pytest
from navbench.ca import *


def test_typical():
    idf = [1, 2, 0, 2, 3, 1]
    bounds, goal = get_idf_ca_bounds(idf)
    assert goal == 2
    assert bounds == (1, 4)
    assert get_idf_ca(idf) == 3


def test_no_left():
    idf = [0, 2, 1]
    bounds, goal = get_idf_ca_bounds(idf)
    assert goal == 0
    assert bounds == (0, 1)
    assert get_idf_ca(idf) == 1


def test_no_right():
    idf = [1, 2, 0]
    bounds, goal = get_idf_ca_bounds(idf)
    assert goal == 2
    assert bounds == (1, 2)
    assert get_idf_ca(idf) == 1


def test_empty():
    with pytest.raises(ValueError):
        get_idf_ca([])


def test_single():
    assert get_idf_ca([0]) == 0


def test_infinite_left():
    idf = [1, 1, 0, 2, 1]
    bounds, goal = get_idf_ca_bounds(idf)
    assert goal == 2
    assert bounds == (None, 3)


def test_infinite_right():
    idf = [1, 2, 0, 1, 1]
    bounds, goal = get_idf_ca_bounds(idf)
    assert goal == 2
    assert bounds == (1, None)


def test_medfilt_toosmall():
    with pytest.raises(ValueError):
        get_idf_ca([1, 2, 0, 2, 1], filter_size=3)


def test_medfilt_right():
    assert get_idf_ca([0, 1, 2, 1, 3, 1], filter_size=3) == 3


def test_medfilt_left():
    assert get_idf_ca([1, 3, 1, 2, 1, 0], filter_size=3) == 3


def test_medfilt_both():
    assert get_idf_ca([1, 3, 1, 2, 1, 0, 1, 2, 1, 3, 1], filter_size=3) == 6
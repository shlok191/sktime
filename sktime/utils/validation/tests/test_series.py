#!/usr/bin/env python3 -u
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
"""Test series module."""

__author__ = ["benheid"]

import numpy as np
import pytest

from sktime.tests.test_switch import run_test_for_class
from sktime.utils.validation.series import check_equal_time_index

first_arrays = (np.random.random(1000),)
second_arrays = (np.random.random(1000),)


@pytest.mark.skipif(
    not run_test_for_class(check_equal_time_index),
    reason="Run if tested function has changed.",
)
@pytest.mark.parametrize("first_array", first_arrays)
@pytest.mark.parametrize("second_array", second_arrays)
def test_check_equal_time_index(first_array, second_array):
    """Test that fh validation throws an error with empty container."""
    check_equal_time_index(first_array, second_array)

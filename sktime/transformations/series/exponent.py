#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
"""Implements transformers raise time series to user provided exponent."""

__author__ = ["Ryan Kuhns"]
__all__ = ["ExponentTransformer", "SqrtTransformer"]

import numpy as np
import pandas as pd

from sktime.transformations.base import BaseTransformer


class ExponentTransformer(BaseTransformer):
    """Apply exponent transformation to a timeseries.

    Transformation raises input series to the `power` provided. By default,
    when offset="auto", a series with negative values is shifted prior to the
    exponentiation to avoid potential errors of applying certain fractional
    exponents to negative values.

    Parameters
    ----------
    power : int or float, default=0.5
        The power to raise the input timeseries to.

    offset : "auto", int or float, default="auto"
        Offset to be added to the input timeseries prior to raising
        the timeseries to the given `power`. If "auto" the series is checked to
        determine if it contains negative values. If negative values are found
        then the offset will be equal to the absolute value of the most negative
        value. If not negative values are present the offset is set to zero.
        If an integer or float value is supplied it will be used as the offset.

    Attributes
    ----------
    power : int or float
        User supplied power.

    offset : int or float
        User supplied offset value.

    See Also
    --------
    BoxCoxTransformer :
        Applies Box-Cox power transformation. Can help normalize data and
        compress variance of the series.
    LogTransformer :
        Transformer input data using natural log. Can help normalize data and
        compress variance of the series.
    sktime.transformations.series.exponent.SqrtTransformer :
        Transform input data by taking its square root. Can help compress
        variance of input series.

    Notes
    -----
    For an input series `Z` the exponent transformation is defined as
    :math:`(Z + offset)^{power}`.

    Examples
    --------
    >>> from sktime.transformations.series.exponent import ExponentTransformer
    >>> from sktime.datasets import load_airline
    >>> y = load_airline()
    >>> transformer = ExponentTransformer()
    >>> y_transform = transformer.fit_transform(y)
    """

    _tags = {
        "scitype:transform-input": "Series",
        # what is the scitype of X: Series, or Panel
        "scitype:transform-output": "Series",
        # what scitype is returned: Primitives, Series, Panel
        "scitype:instancewise": True,  # is this an instance-wise transform?
        "X_inner_mtype": ["pd.DataFrame", "pd.Series"],
        # which mtypes do _fit/_predict support for X?
        "y_inner_mtype": "None",  # which mtypes do _fit/_predict support for y?
        "fit-in-transform": False,
        "transform-returns-same-time-index": True,
        "univariate-only": False,
        "capability:inverse_transform": True,
    }

    def __init__(self, power=0.5, offset="auto"):
        self.power = power
        self.offset = offset
        self._offset_value = None

        super(ExponentTransformer, self).__init__()

    def _fit(self, X, y=None):
        """
        Fit transformer to X and y.

        private _fit containing the core logic, called from fit

        Parameters
        ----------
        X : pd.Series or pd.DataFrame
            Data to fit transform to
        y : ignored argument for interface compatibility
            Additional data, e.g., labels for transformation

        Returns
        -------
        self: a fitted instance of the estimator
        """
        Z = X
        if not isinstance(self.power, (int, float)):
            raise ValueError(
                f"Expected `power` to be int or float, but found {type(self.power)}."
            )
        if self.offset == "auto":
            if isinstance(Z, pd.Series):
                min_values = Z.min()
            else:
                min_values = Z.min(axis=0).values.reshape(1, -1)
            self._offset_value = np.where(min_values < 0, np.abs(min_values), 0)

        elif isinstance(self.offset, (int, float)):
            self._offset_value = self.offset

        else:
            raise ValueError(
                f"Expected `offset` to be int or float, but found {type(self.offset)}."
            )

        return self

    def _transform(self, X, y=None):
        """Transform X and return a transformed version.

        private _transform containing the core logic, called from transform

        Parameters
        ----------
        X : pd.Series or pd.DataFrame
            Data to be transformed
        y : ignored argument for interface compatibility
            Additional data, e.g., labels for transformation

        Returns
        -------
        Xt : pd.Series or pd.DataFrame, same type as X
            transformed version of X
        """
        Zt = X.copy()
        Xt = np.power(Zt + self._offset_value, self.power)

        return Xt

    def _inverse_transform(self, X, y=None):
        """Logic used by `inverse_transform` to reverse transformation on `X`.

        Parameters
        ----------
        X : pd.Series or pd.DataFrame
            Data to be inverse transformed
        y : ignored argument for interface compatibility
            Additional data, e.g., labels for transformation

        Returns
        -------
        Xt : pd.Series or pd.DataFrame, same type as X
            inverse transformed version of X
        """
        Z_inv = X.copy()
        Xt = np.power(Z_inv, 1.0 / self.power) - self._offset_value
        return Xt


class SqrtTransformer(ExponentTransformer):
    """Apply square root transformation to a timeseries.

    Transformation take the square root of the input series. By default,
    when offset="auto", a series with negative values is shifted prior to the
    exponentiation to avoid potential errors of applying square root
    transformation to negative values.

    Parameters
    ----------
    offset : "auto", int or float, default="auto"
        Offset to be added to the input timeseries prior to raising
        the timeseries to the given `power`. If "auto" the series is checked to
        determine if it contains negative values. If negative values are found
        then the offset will be equal to the absolute value of the most negative
        value. If not negative values are present the offset is set to zero.
        If an integer or float value is supplied it will be used as the offset.

    Attributes
    ----------
    offset : int or float
        User supplied offset value.

    See Also
    --------
    BoxCoxTransformer :
        Applies Box-Cox power transformation. Can help normalize data and
        compress variance of the series.
    LogTransformer :
        Transformer input data using natural log. Can help normalize data and
        compress variance of the series.
    sktime.transformations.series.exponent.ExponentTransformer :
        Transform input data by raising it to an exponent. Can help compress
        variance of series if a fractional exponent is supplied.

    Notes
    -----
    For an input series `Z` the square root transformation is defined as
    :math:`(Z + offset)^{0.5}`.

    Examples
    --------
    >>> from sktime.transformations.series.exponent import SqrtTransformer
    >>> from sktime.datasets import load_airline
    >>> y = load_airline()
    >>> transformer = SqrtTransformer()
    >>> y_transform = transformer.fit_transform(y)
    """

    def __init__(self, offset="auto"):
        super().__init__(power=0.5, offset=offset)

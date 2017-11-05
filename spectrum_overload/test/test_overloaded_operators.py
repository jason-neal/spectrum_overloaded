#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import given

from spectrum_overload import Spectrum, SpectrumError


#######################################################
#    Overloading Operators
#######################################################
@given(st.lists(st.integers(min_value=-100000, max_value=100000), min_size=1),
       st.integers(min_value=-1000000, max_value=1000000),
       st.integers(min_value=-1000000, max_value=1000000), st.booleans())
def test_overload_add_integers_with_same_xaxis(x1, y1, y2, calib):
    x1 = np.asarray(x1)
    y1 *= x1
    y2 *= x1

    spec1 = Spectrum(flux=y1, xaxis=x1, calibrated=calib)
    spec2 = Spectrum(flux=y2, xaxis=x1, calibrated=calib)

    spec3 = spec1 + spec2
    spec4 = sum([spec1, spec2])
    spec5 = sum([spec1, spec2, spec3, spec4])
    summed = np.asarray(y1) + np.asarray(y2)
    npsummed = np.asarray(y1) + np.asarray(y2)
    # Assert the flux values are summed togther
    assert np.all(spec3.flux == summed)
    assert np.all(spec3.flux == spec4.flux)
    assert np.all(spec4.flux == summed)
    assert np.all(spec4.flux == npsummed)
    assert np.all(spec5.flux == 3 * summed)

    # Assert calibration has stayed the same.
    assert np.allclose(spec4.calibrated, spec1.calibrated)
    assert np.allclose(spec4.calibrated, spec3.calibrated)
    assert np.allclose(spec3.calibrated, spec2.calibrated)

# Try with floats


@given(st.lists(st.floats(min_value=1e-3, max_value=1e7,
       allow_infinity=False), min_size=1,), st.floats(min_value=1e-3),
       st.floats(min_value=1e-3), st.booleans())
def test_overload_add_with_same_xaxis(x1, y1, y2, calib):
    x1 = np.asarray(x1)
    y1 *= x1
    y2 *= x1
    spec1 = Spectrum(flux=y1, xaxis=x1, calibrated=calib)
    spec2 = Spectrum(flux=y2, xaxis=x1, calibrated=calib)

    spec3 = spec1 + spec2
    spec4 = sum([spec1, spec2])
    # Assert the flux values are summed together
    assert np.allclose(spec3.flux, np.asarray(y1) + np.asarray(y2))
    assert np.allclose(spec3.flux, spec4.flux)

    # Assert calibration has stayed the same.
    assert np.allclose(spec4.calibrated, spec1.calibrated)
    assert np.allclose(spec4.calibrated, spec3.calibrated)
    assert np.allclose(spec3.calibrated, spec2.calibrated)
    # Need to also check on xaxis after the calibration has been performed.


@given(st.lists(st.floats(min_value=1e-3, max_value=1e7,
       allow_infinity=False), min_size=1,), st.floats(min_value=-1e7,
       max_value=1e7), st.floats(min_value=-1e10, max_value=1e10),
       st.booleans())
def test_overload_sub_with_same_xaxis(x1, y1, y2, calib):
    x1 = np.asarray(x1)
    y1 *= x1
    y2 *= x1
    spec1 = Spectrum(flux=y1, xaxis=x1, calibrated=calib)
    spec2 = Spectrum(flux=y2, xaxis=x1, calibrated=calib)
    spec_sub = spec1 - spec2

    assert np.allclose(spec_sub.flux, np.asarray(y1) - np.asarray(y2))

    # Testing some other random things between them
    assert np.all(spec_sub.xaxis == spec2.xaxis)
    assert np.all(spec_sub.xaxis == spec1.xaxis)
    assert spec_sub.calibrated == spec1.calibrated
    assert spec_sub.calibrated == spec2.calibrated
    # May want to record the transformation in the header
    assert spec_sub.header == spec1.header     # Might not want this later.


@given(st.lists(st.floats(min_value=1e-3, max_value=1e7,
       allow_infinity=False), min_size=1,), st.floats(min_value=-1e7,
       max_value=1e7), st.floats(min_value=-1e10, max_value=1e10),
       st.booleans())
def test_overload_mul_with_same_xaxis(x1, y1, y2, calib):
    x1 = np.asarray(x1)
    y1 *= x1
    y2 *= x1
    spec1 = Spectrum(flux=y1, xaxis=x1, calibrated=calib)
    spec2 = Spectrum(flux=y2, xaxis=x1, calibrated=calib)
    spec_mul = spec1 * spec2

    assert np.allclose(spec_mul.flux, np.asarray(y1) * np.asarray(y2))

    # Testing some other random things between them
    assert np.all(spec_mul.xaxis == spec2.xaxis)
    assert np.all(spec_mul.xaxis == spec1.xaxis)
    assert spec_mul.calibrated == spec1.calibrated
    assert spec_mul.calibrated == spec2.calibrated
    # May want to record the transformation in the header
    assert spec_mul.header == spec1.header   # Might not want this later.


@given(st.lists(st.floats(min_value=1e-3, max_value=1e7,
       allow_infinity=False), min_size=1,), st.floats(min_value=1e-3,
       max_value=1e7, allow_infinity=False), st.floats(min_value=-1e10,
       max_value=1e10, allow_infinity=False), st.booleans())
def test_overload_truediv_with_same_xaxis(x1, y1, y2, calib):
    x1 = np.asarray(x1)
    y1 *= x1
    y2 *= x1
    spec1 = Spectrum(flux=y1, xaxis=x1, calibrated=calib)
    spec2 = Spectrum(flux=y2, xaxis=x1, calibrated=calib)
    spec_truediv = spec1 / spec2

    assert np.allclose(spec_truediv.flux, np.asarray(y1) / np.asarray(y2))

    # Testing some other random things between them
    assert np.all(spec_truediv.xaxis == spec2.xaxis)
    assert np.all(spec_truediv.xaxis == spec1.xaxis)
    assert spec_truediv.calibrated == spec1.calibrated
    assert spec_truediv.calibrated == spec2.calibrated
    # May want to record the transformation in the header
    assert spec_truediv.header == spec1.header  # Might not want this later.


def test_truediv_with_number():
    # To test if can divide flux by a number
    number = 0.3
    flux_arr = np.array([1, 2, 3, 2.3, 4.5])
    spec1 = Spectrum(flux=flux_arr, xaxis=[1, 1.1, 1.2, 2.1, 4],
                     calibrated=True)

    spec_truediv = spec1 / number

    assert np.all(spec_truediv.flux == flux_arr / number)


def test_len_works():
    # Test len works
    spec1 = Spectrum([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    assert len(spec1) == 5


def test_for_raise_die_to_calibration_mismatch():
    # Try catch my raise
    s1 = Spectrum([1], [2], calibrated=True)
    s2 = Spectrum([1], [2], calibrated=False)
    # This will fail untill I work out errors more
    with pytest.raises(SpectrumError):
        s1 + s2
    with pytest.raises(SpectrumError):
        s1 - s2
    with pytest.raises(SpectrumError):
        s1 * s2
    with pytest.raises(SpectrumError):
        s1 / s2


def test_overload_pow():
    # Trying to catch error with raises
    power = 2
    spec1 = Spectrum([1, 2, 3, 4], [2, 3, 4, 5], None, True)
    spec2 = Spectrum([1, 2, 3, 4], [1, 3, 1, 4], None, True)
    # Can test when things are not supposed to work :)
    with pytest.raises(TypeError):
        spec1 ** spec2
    with pytest.raises(TypeError):
        # Does not accept lists
        spec1 ** [1]                # This should fail
    with pytest.raises(TypeError):
        spec1 ** [1, 2]              # This should fail also
    with pytest.raises(TypeError):
        # Does not accept lists
        spec1 ** (2,)               # This should fail as it is a tuple
    with pytest.raises(ValueError):
        spec1 ** np.array([1, 2])   # too many values
    # Should also test that something works
    spec4 = spec1 ** power
    assert np.all(spec4.flux == np.array([1, 4, 9, 16]))  # flux is squared
    assert np.all(spec4.xaxis == spec1.xaxis)  # xaxis stays the same


@given(st.lists(st.floats(min_value=1e-3, max_value=1e7,
       allow_infinity=False), min_size=1,), st.floats(min_value=1e-3,
       max_value=1e7, allow_infinity=False), st.floats(min_value=1e-7,
       max_value=1e10, allow_infinity=False), st.integers(min_value=1,
       max_value=int(1e5)))
def test_add_sub_mult_divide_by_numbers(x, y, float1, int1):
    y *= np.array(x)   # turn to array for operations
    spec = Spectrum(flux=y, xaxis=x)
    # Add by a float
    spec_add = spec + float1
    spec_add_int = spec + int1
    assert np.all(spec_add.flux == y + float1)
    assert np.all(spec_add_int.flux == y + int1)
    # Subtract by an int
    spec_sub = spec - float1
    spec_sub_int = spec - int1
    assert np.all(spec_sub.flux == y - float1)
    assert np.all(spec_sub_int.flux == y - int1)
    # Multiply by an int
    spec_mul = spec * float1
    spec_mul_int = spec * int1
    assert np.all(spec_mul.flux == y * float1)
    assert np.all(spec_mul_int.flux == y * int1)
    # Divide by an int
    spec_truediv = spec / float1
    spec_truediv_int = spec / int1
    assert np.all(spec_truediv.flux == y / float1)
    assert np.all(spec_truediv_int.flux == y / int1)


def test_unitary_operators():
    """Test __pos__ and __neg__ operators."""
    a = np.array([1, 2, -3, 4])
    b = np.array([1, 2, 3, 4])
    spec = Spectrum(a, b)
    spec1 = +spec
    assert np.all(spec1.flux == a)
    assert np.all(spec1.flux == spec.flux)
    spec2 = -spec
    assert np.all(spec2.flux == -a)
    assert np.all(spec2.flux == -spec1.flux)


def test_abs_operator():
    """Test absolute value of flux."""
    spec = Spectrum([-1, 2, -3.2, 4], [2, 3, 4, 5])
    abs_spec = abs(spec)
    abs_spec2 = abs(abs_spec)
    assert np.all(abs_spec.flux == np.array([1, 2, 3.2, 4]))
    assert np.all(abs_spec.flux == abs_spec2.flux)


def test_addition_with_interpolation():
    s1 = Spectrum([1, 2, 2, 1], [2, 4, 8, 10])
    x = np.array([1, 5, 7, 8, 12])
    s2 = Spectrum([1, 2, 1, 2, 1], x)
    d1 = s1 + s2
    d2 = s2 + s1
    assert np.all(d2.xaxis == x)  # d has axis of t
    assert np.all(d1.xaxis == s1.xaxis)
    assert np.all(d2.xaxis == s2.xaxis)
    assert len(d1) != len(d2)   # due to different length of s1 and s2

    # Values in one that are outside range are filled with nans
    s3 = Spectrum([1, 3, 1, 2, 3, 2], [3, 4, 5, 6, 7, 8])
    s4 = Spectrum([1, 2, 1, 2, 1, 2, 1], [4, 5, 6, 7, 8, 9, 10])
    d3 = s3 + s4
    d4 = s4 + s3
    assert np.all(d3.xaxis == s3.xaxis)
    assert np.all(d4.xaxis == s4.xaxis)
    # Difficult to get nans to equal so using isnan inverted
    d3notnan = np.invert(np.isnan(d3.flux))
    assert np.allclose(d3.flux[d3notnan],
                       np.array([np.nan, 4, 3, 3, 5, 3])[d3notnan])
    d4notnan = np.invert(np.isnan(d4.flux))
    assert np.allclose(d4.flux[d4notnan],
                       np.array([4, 3, 3, 5, 3, np.nan, np.nan])[d4notnan])
    s5 = Spectrum([1, 2, 1, 2, 1], [50, 51, 52, 53, 54])
    # xaxis of both Spectrum do not overlap
    with pytest.raises(ValueError):
        s5 + s1
    with pytest.raises(ValueError):
        s1 + s5


def test_subtraction_with_interpolation():
    s1 = Spectrum([1, 2, 2, 1], [2, 4, 8, 10])
    x = np.array([1, 5, 7, 8, 12])
    s2 = Spectrum([1, 2, 1, 2, 1], x)
    d1 = s1 - s2
    d2 = s2 - s1
    assert np.all(d2.xaxis == x)  # d has axis of t
    assert np.all(d1.xaxis == s1.xaxis)
    assert np.all(d2.xaxis == s2.xaxis)
    assert len(d1) != len(d2)   # due to different length of s1 and s2

    # Values in one that are outside range are filled with nans
    s3 = Spectrum([1, 2, 1, 2, 1, 2], [3, 4, 5, 6, 7, 8])
    s4 = Spectrum([1, 2, 1, 2, 1, 2, 1], [4, 5, 6, 7, 8, 9, 10])
    d3 = s3 - s4
    d4 = s4 - s3
    assert np.all(d3.xaxis == s3.xaxis)
    assert np.all(d4.xaxis == s4.xaxis)
    # Difficult to get nans to equal so using isnan inverted
    d3notnan = np.invert(np.isnan(d3.flux))
    assert np.allclose(d3.flux[d3notnan],
                       np.array([np.nan, 1, -1, 1, -1, 1])[d3notnan])
    d4notnan = np.invert(np.isnan(d4.flux))
    assert np.allclose(d4.flux[d4notnan],
                       np.array([-1, 1, -1, 1, -1, np.nan, np.nan])[d4notnan])
    s5 = Spectrum([1, 2, 1, 2, 1], [50, 51, 52, 53, 54])
    # xaxis of both Spectrum do not overlap
    with pytest.raises(ValueError):
        s5 - s1
    with pytest.raises(ValueError):
        s1 - s5


def test_multiplication_with_interpolation():
    s1 = Spectrum([1, 2, 2, 1], [2, 4, 8, 10])
    x = np.array([1, 5, 7, 8, 12])
    s2 = Spectrum([1, 2, 1, 2, 1], x)
    d1 = s1 * s2
    d2 = s2 * s1
    assert np.all(d2.xaxis == x)  # d has axis of t
    assert np.all(d1.xaxis == s1.xaxis)
    assert np.all(d2.xaxis == s2.xaxis)
    assert len(d1) != len(d2)   # due to different length of s1 and s2

    # Values in one that are outside range are filled with nans
    s3 = Spectrum([1, 3, 1, 2, 3, 2], [3, 4, 5, 6, 7, 8])
    s4 = Spectrum([1, 2, 1, 2, 1, 2, 1], [4, 5, 6, 7, 8, 9, 10])
    d3 = s3 * s4
    d4 = s4 * s3
    assert np.all(d3.xaxis == s3.xaxis)
    assert np.all(d4.xaxis == s4.xaxis)
    # Difficult to get nans to equal so using isnan inverted
    d3notnan = np.invert(np.isnan(d3.flux))
    assert np.allclose(d3.flux[d3notnan],
                       np.array([np.nan, 3, 2, 2, 6, 2])[d3notnan])
    d4notnan = np.invert(np.isnan(d4.flux))
    assert np.allclose(d4.flux[d4notnan],
                       np.array([3, 2, 2, 6, 2, np.nan, np.nan])[d4notnan])
    s5 = Spectrum([1, 2, 1, 2, 1], [50, 51, 52, 53, 54])
    # xaxis of both Spectrum do not overlap
    with pytest.raises(ValueError):
        s5 * s1
    with pytest.raises(ValueError):
        s1 * s5


def test_true_division_with_interpolation():
    s1 = Spectrum([1, 2, 2, 1], [2, 4, 8, 10])
    x = np.array([1, 5, 7, 8, 12])
    s2 = Spectrum([1, 2, 1, 2, 1], x)
    d1 = s1 / s2
    d2 = s2 / s1
    assert np.all(d2.xaxis == x)  # d has axis of t
    assert np.all(d1.xaxis == s1.xaxis)
    assert np.all(d2.xaxis == s2.xaxis)
    assert len(d1) != len(d2)   # due to different length of s1 and s2

    # Values in one that are outside range are filled with nans
    s3 = Spectrum([1, 2, 1, 2, 1, 2], [3, 4, 5, 6, 7, 8])
    s4 = Spectrum([1, 2, 1, 2, 1, 2, 1], [4, 5, 6, 7, 8, 9, 10])
    d3 = s3 / s4
    d4 = s4 / s3
    assert np.all(d3.xaxis == s3.xaxis)
    assert np.all(d4.xaxis == s4.xaxis)
    # Difficult to get nans to equal so using isnan inverted
    d3notnan = np.invert(np.isnan(d3.flux))
    assert np.allclose(d3.flux[d3notnan],
                       np.array([np.nan, 2, .5, 2, .5, 2])[d3notnan])
    d4notnan = np.invert(np.isnan(d4.flux))
    assert np.allclose(d4.flux[d4notnan],
                       np.array([.5, 2, .5, 2, .5, np.nan, np.nan])[d4notnan])
    s5 = Spectrum([1, 2, 1, 2, 1], [50, 51, 52, 53, 54])
    # xaxis of both Spectrum do not overlap
    with pytest.raises(ValueError):
        s5 / s1
    with pytest.raises(ValueError):
        s1 / s5


def test_value_error_when_spectra_do_not_overlap():
    s = Spectrum([1, 2, 1, 2, 1], [2, 4, 6, 8, 10])
    u = Spectrum([1, 2, 1, 2], [50, 51, 52, 53])

    with pytest.raises(ValueError):
        s + u
    with pytest.raises(ValueError):
        s - u
    with pytest.raises(ValueError):
        s / u
    with pytest.raises(ValueError):
        s * u


@pytest.mark.parametrize("badly_typed", [
    "Test String",
    [1, 2, 3, 4, 5],
    [2, 3, "4", 5, 6],
    (1, 2, "3", 6, 7),
    {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5},
    {1, 4, 4, 2, 5},
])
def test_operators_with_bad_types(badly_typed):
    s = Spectrum([1, 2, 1, 2, 1], [2, 4, 6, 8, 10])
    with pytest.raises(TypeError):
        s + badly_typed
    with pytest.raises(TypeError):
        s - badly_typed
    with pytest.raises(TypeError):
        s * badly_typed
    with pytest.raises(TypeError):
        s / badly_typed


@pytest.mark.parametrize("badly_typed", [
    "Test String",
    # [1, 2, 3, 4, 5],
    # [2, 3, "4"],
    # (1, 2, "3"),
    {"1": 1, "2": 2, "3": 3},
    # {1, 2, 3, 1, 4, 4, 2, 5},  # set literal faster than set()
])
def test_assignment_with_bad_types(badly_typed):
    # Need to improve checking of what can pass into spectrum
    with pytest.raises(TypeError):
        Spectrum(flux=None, xaxis=badly_typed)
    with pytest.raises(TypeError):
        Spectrum(flux=badly_typed)


def test_spectra_stay_the_same_after_operations():
    """After a operation of two spectra...

    e.g. a/b both a and b should
    remain the same unless specifically defined such as a = a + b

    """
    a = Spectrum(xaxis=[1, 2, 3, 4], flux=[5, 6, 7, 8])
    b = Spectrum(xaxis=[1, 2, 3, 4], flux=[1, 2, 3, 4])
    c = a.copy()
    d = b.copy()

    e = c + d
    f = c - d
    g = d * c
    h = d / c
    # c and d still the same
    assert a == c
    assert b == d
    assert e != c  and e != d
    assert f != c and f != d
    assert g != c and g != d
    assert h != c and h != d


def test_spectra_not_the_same_when_reassigned():
    """After a operation of two spectra...

    e.g. a/b both a and b should
    remain the same unless specifically defined such as a = a + b

    """
    a = Spectrum(xaxis=[1, 2, 3, 4], flux=[5, 6, 7, 8])
    b = Spectrum(xaxis=[1, 2, 3, 4], flux=[1, 2, 3, 4])
    c = a.copy()
    d = b.copy()
    e = a.copy()
    f = b.copy()

    c = c + b
    d = d - c
    e = e * 2
    f /= 6
    # changes spectra are different
    assert c != a
    assert d != b
    assert e != a
    assert f != b


def test_xaxis_type_error_init_check():
    # Test that passing None to xaxis when flux doesn't have a length
    # results in just setting to None
    s = Spectrum(np.nan, None)
    assert s.xaxis is None
    s.flux = [1, 1.1]   # has length
    s.xaxis = None      # xaxis turns into range(len(s.flux))
    assert s.xaxis is not None
    print(s.xaxis)
    assert np.all(s.xaxis == np.array([0, 1]))
    s.flux = 1          # 1 has no length
    s.xaxis = None
    assert s.xaxis is None
    s.flux = np.inf     # np.inf has no length
    s.xaxis = None
    assert s.xaxis is None


def test_wave_selection_with_ill_defined_xaxis():
    # if xaxis is None
    s = Spectrum()
    s.flux = [1, 2, 3, 4, 3, 2, 1]
    with pytest.raises(TypeError):
        s.wav_select(1, 8)
    # dealing when xaxis is empty []
    s = Spectrum()
    s.flux = []
    s.xaxis = []
    s.wav_select(1, 8)
    assert np.all(s.flux == np.array([]))        # s Didn't change
    assert np.all(s.xaxis == np.array([]))       # s Didn't change
    new_flux = [1, 2, 3, 4]
    s.flux = new_flux     # different flux but same xaxis
    s.wav_select(1, 8)
    assert np.all(s.flux == np.array(new_flux))  # s Didn't change
    assert np.all(s.xaxis == np.array([]))       # s Didn't change


def test_zero_division():
    s = Spectrum(flux=[1, 2, 3, 4], xaxis=[1, 2, 3, 4])
    t = Spectrum(flux=[1, 2, 0, 4], xaxis=[1, 2, 3, 4])

    divide = s / t
    print(divide.xaxis)
    print(divide.flux)
    notnan = np.invert(np.isinf(divide.flux))
    print(divide.flux[2])
    assert np.isinf(divide.flux[2])
    assert np.all(divide.flux[notnan] == [1, 1, 1])
    div2 = s / 0
    assert np.all(np.isinf(div2.flux))  # div by zero goes to np.inf
    div3 = s / np.float(0)
    assert np.all(np.isinf(div3.flux))  # div by zero goes to np.inf


def test_addition_preserves_header():
    hdr = {"this": "header", "value": 2}
    s = Spectrum([1, 2, 3, 4], [1, 2, 3, 4], header=hdr)
    s += 1

    assert np.all(s.flux == [2, 3, 4, 5])
    assert s.header is not None
    assert s.header == hdr


def test_subtraction_preserves_header():
    hdr = {"this": "header", "value": 2}
    s = Spectrum([1, 2, 3, 4], [1, 2, 3, 4], header=hdr)
    s -= 1

    assert np.all(s.flux == [0, 1, 2, 3])
    assert s.header is not None
    assert s.header == hdr


def test_multiplication_preserves_header():
    hdr = {"this": "header", "value": 2}
    s = Spectrum([1, 2, 3, 4], [1, 2, 3, 4], header=hdr)
    s *= 2

    assert np.all(s.flux == [2, 4, 6, 8])
    assert s.header is not None
    assert s.header == hdr


def test_division_preserves_header():
    hdr = {"this": "header", "value": 2}
    s = Spectrum(xaxis=[1, 2, 3, 4], flux=[2, 4, 6, 8], header=hdr)
    s /= 2

    assert np.all(s.flux == [1, 2, 3, 4])
    assert s.header is not None
    assert s.header == hdr

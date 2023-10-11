import pytest
import six

import escpos.printer as printer
from escpos.constants import PrinterCommands
from escpos.exceptions import SetVariableError

cmdset = PrinterCommands()
TXT_NORMAL, TXT_STYLE, TXT_SIZE, SET_FONT = cmdset.TXT_NORMAL, cmdset.TXT_STYLE, cmdset.TXT_SIZE, cmdset.set_font

def test_default_values_with_default():
    """Default test, please copy and paste this block to test set method calls"""
    instance = printer.Dummy()
    instance.set_with_default()

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["normal"],  # Normal text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


def test_default_values():
    """Default test"""
    instance = printer.Dummy()
    instance.set()

    assert instance.output == b""


# Size tests


def test_set_size_2h():
    instance = printer.Dummy()
    instance.set_with_default(double_height=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["2h"],  # Double height text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


def test_set_size_2h_no_default():
    instance = printer.Dummy()
    instance.set(double_height=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["2h"],  # Double height text size
    )

    assert instance.output == b"".join(expected_sequence)


def test_set_size_2w():
    instance = printer.Dummy()
    instance.set_with_default(double_width=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["2w"],  # Double width text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


def test_set_size_2w_no_default():
    instance = printer.Dummy()
    instance.set(double_width=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["2w"],  # Double width text size
    )

    assert instance.output == b"".join(expected_sequence)


def test_set_size_2x():
    instance = printer.Dummy()
    instance.set_with_default(double_height=True, double_width=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["2x"],  # Double text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


def test_set_size_2x_no_default():
    instance = printer.Dummy()
    instance.set(double_width=True, double_height=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["2x"],  # Quad area text size
    )

    assert instance.output == b"".join(expected_sequence)


def test_set_size_custom():
    instance = printer.Dummy()
    instance.set_with_default(custom_size=True, width=8, height=7)

    expected_sequence = (
        TXT_SIZE,  # Custom text size, no normal reset
        six.int2byte(TXT_STYLE["width"][8] + TXT_STYLE["height"][7]),
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


@pytest.mark.parametrize("width", [1, 8])
@pytest.mark.parametrize("height", [1, 8])
def test_set_size_custom_no_default(width, height):
    instance = printer.Dummy()
    instance.set(custom_size=True, width=width, height=height)

    expected_sequence = (
        TXT_SIZE,  # Custom text size, no normal reset
        six.int2byte(TXT_STYLE["width"][width] + TXT_STYLE["height"][height]),
    )

    assert instance.output == b"".join(expected_sequence)


@pytest.mark.parametrize("width", [None, 0, 9, 10, 4444])
@pytest.mark.parametrize("height", [None, 0, 9, 10, 4444])
def test_set_size_custom_invalid_input(width, height):
    instance = printer.Dummy()
    with pytest.raises(SetVariableError):
        instance.set(custom_size=True, width=width, height=height)


# Flip


def test_set_flip():
    instance = printer.Dummy()
    instance.set_with_default(flip=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["normal"],  # Normal text size
        TXT_STYLE["flip"][True],  # Flip ON
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


def test_set_flip_no_default():
    instance = printer.Dummy()
    instance.set(flip=True)

    expected_sequence = (TXT_STYLE["flip"][True],)  # Flip ON

    assert instance.output == b"".join(expected_sequence)


# Smooth


def test_smooth():
    instance = printer.Dummy()
    instance.set_with_default(smooth=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["normal"],  # Normal text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][True],  # Smooth ON
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


# Type


def test_set_bold():
    instance = printer.Dummy()
    instance.set_with_default(bold=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["normal"],  # Normal text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][True],  # Bold ON
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


def test_set_underline():
    instance = printer.Dummy()
    instance.set_with_default(underline=1)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["normal"],  # Normal text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][1],  # Underline ON, type 1
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


def test_set_underline2():
    instance = printer.Dummy()
    instance.set_with_default(underline=2)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["normal"],  # Normal text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][2],  # Underline ON, type 2
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


# Align


def test_align_center():
    instance = printer.Dummy()
    instance.set_with_default(align="center")

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["normal"],  # Normal text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["center"],  # Align center
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


def test_align_right():
    instance = printer.Dummy()
    instance.set_with_default(align="right")

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["normal"],  # Normal text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["right"],  # Align right
        TXT_STYLE["invert"][False],  # Inverted OFF
    )

    assert instance.output == b"".join(expected_sequence)


# Densities


def test_densities():
    for density in range(8):
        instance = printer.Dummy()
        instance.set_with_default(density=density)

        expected_sequence = (
            TXT_NORMAL,
            TXT_STYLE["size"]["normal"],  # Normal text size
            TXT_STYLE["flip"][False],  # Flip OFF
            TXT_STYLE["smooth"][False],  # Smooth OFF
            TXT_STYLE["bold"][False],  # Bold OFF
            TXT_STYLE["underline"][0],  # Underline OFF
            SET_FONT(b"\x00"),  # Default font
            TXT_STYLE["align"]["left"],  # Align left
            TXT_STYLE["density"][density],  # Custom density from 0 to 8
            TXT_STYLE["invert"][False],  # Inverted OFF
        )

        assert instance.output == b"".join(expected_sequence)


# Invert


def test_invert():
    instance = printer.Dummy()
    instance.set_with_default(invert=True)

    expected_sequence = (
        TXT_NORMAL,
        TXT_STYLE["size"]["normal"],  # Normal text size
        TXT_STYLE["flip"][False],  # Flip OFF
        TXT_STYLE["smooth"][False],  # Smooth OFF
        TXT_STYLE["bold"][False],  # Bold OFF
        TXT_STYLE["underline"][0],  # Underline OFF
        SET_FONT(b"\x00"),  # Default font
        TXT_STYLE["align"]["left"],  # Align left
        TXT_STYLE["invert"][True],  # Inverted ON
    )

    assert instance.output == b"".join(expected_sequence)

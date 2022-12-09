#  -*- coding: utf-8 -*-
""" Set of ESC/POS Commands (Constants)

This module contains constants that are described in the esc/pos-documentation.
Since there is no definitive and unified specification for all esc/pos-like printers the constants could later be
moved to `capabilities` as in `escpos-php by @mike42 <https://github.com/mike42/escpos-php>`_.

:author: `Manuel F Martinez <manpaz@bashlinux.com>`_ and others
:organization: Bashlinux and `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2017 Bashlinux and python-escpos
:license: MIT
"""


import six

# Control characters
# as labelled in https://www.novopos.ch/client/EPSON/TM-T20/TM-T20_eng_qr.pdf
NUL = b"\x00"
EOT = b"\x04"
ENQ = b"\x05"
DLE = b"\x10"
DC4 = b"\x14"
CAN = b"\x18"
ESC = b"\x1b"
FS = b"\x1c"
GS = b"\x1d"
RS = b"\x1e"

# Feed control sequences
CTL_LF = b"\n"  # Print and line feed
CTL_FF = b"\f"  # Form feed
CTL_CR = b"\r"  # Carriage return
CTL_HT = b"\t"  # Horizontal tab
CTL_SET_HT = ESC + b"\x44"  # Set horizontal tab positions
CTL_VT = b"\v"  # Vertical tab

# Bounds and validation regex for known barcode formats
BARCODE_FORMATS = {
    "UPC-A": ([(11, 12)], "^[0-9]{11,12}$"),
    "UPC-E": ([(7, 8), (11, 12)], "^([0-9]{7,8}|[0-9]{11,12})$"),
    "EAN13": ([(12, 13)], "^[0-9]{12,13}$"),
    "EAN8": ([(7, 8)], "^[0-9]{7,8}$"),
    "CODE39": ([(1, 255)], "^([0-9A-Z \$\%\+\-\.\/]+|\*[0-9A-Z \$\%\+\-\.\/]+\*)$"),
    "ITF": ([(2, 255)], "^([0-9]{2})+$"),
    "NW7": ([(1, 255)], "^[A-Da-d][0-9\$\+\-\.\/\:]+[A-Da-d]$"),
    "CODABAR": ([(1, 255)], "^[A-Da-d][0-9\$\+\-\.\/\:]+[A-Da-d]$"),  # Same as NW7
    "CODE93": ([(1, 255)], "^[\\x00-\\x7F]+$"),
    "CODE128": ([(2, 255)], "^\{[A-C][\\x00-\\x7F]+$"),
    "GS1-128": ([(2, 255)], "^\{[A-C][\\x00-\\x7F]+$"),  # same as CODE128
    "GS1 DATABAR OMNIDIRECTIONAL": ([(13, 13)], "^[0-9]{13}$"),
    "GS1 DATABAR TRUNCATED": ([(13, 13)], "^[0-9]{13}$"),  # same as GS1 omnidirectional
    "GS1 DATABAR LIMITED": ([(13, 13)], "^[01][0-9]{12}$"),
    "GS1 DATABAR EXPANDED": (
        [(2, 255)],
        "^\([0-9][A-Za-z0-9 \!\"\%\&'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\_\{]+$",
    ),
}

# QRCode error correction levels
QR_ECLEVEL_L = 0
QR_ECLEVEL_M = 1
QR_ECLEVEL_Q = 2
QR_ECLEVEL_H = 3

# QRcode models
QR_MODEL_1 = 1
QR_MODEL_2 = 2
QR_MICRO = 3


class PrinterCommands:
    """ keeps constants for printer commands """
    def __init__(self):
        # Printer hardware
        self.HW_INIT = ESC + b"@"                # Clear data in buffer and reset modes
        self.HW_SELECT = ESC + b"=\x01"          # Printer select
        self.HW_RESET = ESC + b"\x3f\x0a\x00"    # Reset printer hardware
                                                 # (TODO: Where is this specified?)
        self.CD_KICK_2 = self._cash_drawer(b"\x00", 50, 50)  # Sends a pulse to pin 2 []
        self.CD_KICK_5 = self._cash_drawer(b"\x01", 50, 50)  # Sends a pulse to pin 5 []
        self.PAPER_FULL_CUT = self._cut_paper(True)          # full cut
        self.PAPER_PART_CUT = self._cut_paper(False)         # partial cut

        # Beep (please note that the actual beep sequence may differ between devices)
        self.BEEP = b"\x07"

        # Panel buttons (e.g. the FEED button)
        self.PANEL_BUTTON_ON = self._panel_button(True)     # enable all panel buttons
        self.PANEL_BUTTON_OFF = self._panel_button(False)   # disable all panel buttons

        # Line display printing
        self.LINE_DISPLAY_OPEN = ESC + b"\x3d\x02"
        self.LINE_DISPLAY_CLEAR = ESC + b"\x40"
        self.LINE_DISPLAY_CLOSE = ESC + b"\x3d\x01"

        # Sheet modes
        # these are actually not documented anywhere, see https://stackoverflow.com/a/64235804
        self.SHEET_SLIP_MODE = ESC + b"\x63\x30\x04"  # slip paper
        self.SHEET_ROLL_MODE = ESC + b"\x63\x30\x01"  # paper roll

        # Text format
        # TODO: Acquire the "ESC/POS Application Programming Guide for Paper Roll
        #       Printers" and tidy up this stuff too.
        self.TXT_SIZE = GS + b"!"

        self.TXT_NORMAL = ESC + b"!\x00"  # Normal text

        self.TXT_STYLE = {
            "bold": {
                False: ESC + b"\x45\x00",  # Bold font OFF
                True: ESC + b"\x45\x01",   # Bold font ON
            },
            "underline": {
                0: ESC + b"\x2d\x00",  # Underline font OFF
                1: ESC + b"\x2d\x01",  # Underline font 1-dot ON
                2: ESC + b"\x2d\x02",  # Underline font 2-dot ON
            },
            "size": {
                "normal": self.TXT_NORMAL + ESC + b"!\x00",  # Normal text
                "2h": self.TXT_NORMAL + ESC + b"!\x10",      # Double height text
                "2w": self.TXT_NORMAL + ESC + b"!\x20",      # Double width text
                "2x": self.TXT_NORMAL + ESC + b"!\x30",      # Quad area text
            },
            "font": {
                "a": self.set_font(b"\x00"),    # Font type A
                "b": self.set_font(b"\x01"),    # Font type B
            },
            "align": {
                "left": ESC + b"\x61\x00",      # Left justification
                "center": ESC + b"\x61\x01",    # Centering
                "right": ESC + b"\x61\x02",     # Right justification
            },
            "invert": {
                True: GS + b"\x42\x01",         # Inverse Printing ON
                False: GS + b"\x42\x00",        # Inverse Printing OFF
            },
            "color": {
                "black": ESC + b"\x72\x00",     # Default Color
                "red": ESC + b"\x72\x01",       # Alternative Color, Usually Red
            },
            "flip": {
                True: ESC + b"\x7b\x01",        # Flip ON
                False: ESC + b"\x7b\x00",       # Flip OFF
            },
            "density": {
                0: GS + b"\x7c\x00",  # Printing Density -50%
                1: GS + b"\x7c\x01",  # Printing Density -37.5%
                2: GS + b"\x7c\x02",  # Printing Density -25%
                3: GS + b"\x7c\x03",  # Printing Density -12.5%
                4: GS + b"\x7c\x04",  # Printing Density  0%
                5: GS + b"\x7c\x08",  # Printing Density +50%
                6: GS + b"\x7c\x07",  # Printing Density +37.5%
                7: GS + b"\x7c\x06",  # Printing Density +25%
                8: GS + b"\x7c\x05",  # Printing Density +12.5%
            },
            "smooth": {
                True: GS + b"\x62\x01",  # Smooth ON
                False: GS + b"\x62\x00",  # Smooth OFF
            },
            "height": {  # Custom text height
                1: 0x00,
                2: 0x01,
                3: 0x02,
                4: 0x03,
                5: 0x04,
                6: 0x05,
                7: 0x06,
                8: 0x07,
            },
            "width": {  # Custom text width
                1: 0x00,
                2: 0x10,
                3: 0x20,
                4: 0x30,
                5: 0x40,
                6: 0x50,
                7: 0x60,
                8: 0x70,
            },
        }

        # Fonts
        self.TXT_FONT_A = self.set_font(b"\x00")  # Font type A
        self.TXT_FONT_B = self.set_font(b"\x01")  # Font type B

        # Spacing
        self.LINESPACING_RESET = ESC + b"2"
        self.LINESPACING_FUNCS = {
            60: ESC + b"A",  # line_spacing/60 of an inch, 0 <= line_spacing <= 85
            360: ESC + b"+",  # line_spacing/360 of an inch, 0 <= line_spacing <= 255
            180: ESC + b"3",  # line_spacing/180 of an inch, 0 <= line_spacing <= 255
        }

        # Prefix to change the codepage. You need to attach a byte to indicate
        # the codepage to use. We use escpos-printer-db as the data source.
        self.CODEPAGE_CHANGE = ESC + b"\x74"

        # Barcode format
        self.BARCODE_TXT_OFF = self._set_barcode_txt_pos(b"\x00")  # HRI barcode chars OFF
        self.BARCODE_TXT_ABV = self._set_barcode_txt_pos(b"\x01")  # HRI barcode chars above
        self.BARCODE_TXT_BLW = self._set_barcode_txt_pos(b"\x02")  # HRI barcode chars below
        self.BARCODE_TXT_BTH = self._set_barcode_txt_pos(b"\x03")  # HRI both above and below
        self.BARCODE_FONT_A = GS + b"f" + b"\x00"  # Font type A for HRI barcode chars
        self.BARCODE_FONT_B = GS + b"f" + b"\x01"  # Font type B for HRI barcode chars
        self.BARCODE_HEIGHT = GS + b"h"  # Barcode Height [1-255]
        self.BARCODE_WIDTH = GS + b"w"  # Barcode Width  [2-6]

        # Barcodes for printing function type A
        BARCODE_TYPE_A = {
            "UPC-A": self._set_barcode_type(0),
            "UPC-E": self._set_barcode_type(1),
            "EAN13": self._set_barcode_type(2),
            "EAN8": self._set_barcode_type(3),
            "CODE39": self._set_barcode_type(4),
            "ITF": self._set_barcode_type(5),
            "NW7": self._set_barcode_type(6),
            "CODABAR": self._set_barcode_type(6),  # Same as NW7
        }

        # Barcodes for printing function type B
        # The first 8 are the same barcodes as type A
        BARCODE_TYPE_B = {
            "UPC-A": self._set_barcode_type(65),
            "UPC-E": self._set_barcode_type(66),
            "EAN13": self._set_barcode_type(67),
            "EAN8": self._set_barcode_type(68),
            "CODE39": self._set_barcode_type(69),
            "ITF": self._set_barcode_type(70),
            "NW7": self._set_barcode_type(71),
            "CODABAR": self._set_barcode_type(71),  # Same as NW7
            "CODE93": self._set_barcode_type(72),
            "CODE128": self._set_barcode_type(73),
            "GS1-128": self._set_barcode_type(74),
            "GS1 DATABAR OMNIDIRECTIONAL": self._set_barcode_type(75),
            "GS1 DATABAR TRUNCATED": self._set_barcode_type(76),
            "GS1 DATABAR LIMITED": self._set_barcode_type(77),
            "GS1 DATABAR EXPANDED": self._set_barcode_type(78),
        }

        self.BARCODE_TYPES = {
            "A": BARCODE_TYPE_A,
            "B": BARCODE_TYPE_B,
        }

        # Status Command
        self.RT_STATUS = DLE + EOT
        self.RT_STATUS_ONLINE = self.RT_STATUS + b"\x01"
        self.RT_STATUS_PAPER = self.RT_STATUS + b"\x04"
        self.RT_MASK_ONLINE = 8
        self.RT_MASK_PAPER = 18
        self.RT_MASK_LOWPAPER = 30
        self.RT_MASK_NOPAPER = 114

    def _cash_drawer(self, m, t1=50, t2=50):
        return ESC + b"p" + m + six.int2byte(t1) + six.int2byte(t2)

    def _cut_paper(self, full):
        return GS + b"V" + b"\x00" if full else b"\x01"

    def _panel_button(self, enable):
        return ESC + b"c5" + six.int2byte(0 if enable else 1)

    def set_codepage(self, page_num):
        return ESC + b"\x74" + six.int2byte(page_num)

    def _set_barcode_txt_pos(self, n):
        return GS + b"H" + n

    def _set_barcode_type(self, m):
        """
        NOTE: This isn't actually an ESC/POS command. It's the common prefix to the
              two "print bar code" commands:
              -  Type A: "GS k <type as integer> <data> NUL"
              -  TYPE B: "GS k <type as letter> <data length> <data>"
              The latter command supports more barcode types
        """
        return GS + b"k" + six.int2byte(m)

    def set_font(self, n):
        return ESC + b"\x4d" + n

    def set_text_size(self, width, height):
        """ set a custom text size """
        size_byte = self.TXT_STYLE["width"][width] + self.TXT_STYLE["height"][height]
        return GS + b"!" + six.int2byte(size_byte)

    def cd_kick_dec_sequence(self, esc, p, m, t1=50, t2=50):
        return six.int2byte(esc) + six.int2byte(p) + six.int2byte(m) + six.int2byte(t1) + six.int2byte(t2)

    def print_and_feed(self, n):
        """ print and feed n lines """
        return ESC + b"d" + six.int2byte(n)


class StarCommands(PrinterCommands):
    """
    overrides commands for star printers
    """
    def __init__(self):
        super().__init__()
        self.TXT_SIZE = b""
        self.TXT_NORMAL = b""
        self.TXT_STYLE = {
            "bold": {
                False: ESC + b"F",  # Bold font OFF
                True: ESC + b"E",  # Bold font ON
            },
            "underline": {
                0: ESC + b"\x2d\x00",  # Underline font OFF
                1: ESC + b"\x2d\x01",  # Underline font 1-dot ON
                2: ESC + b"\x2d\x01",  # Underline font 2-dot ON
            },""
            "size": {
                "normal": ESC + b"i\x00\x00",  # Normal text
                "2h": ESC + b"i\x01\x00",  # Double height text
                "2w": ESC + b"i\x00\x01",  # Double width text
                "2x": ESC + b"i\x01\x01",  # Quad area text
            },
            "font": {
                "a": self.set_font(b"\x00"),   # Font type A
                "b": self.set_font(b"\x01"),   # Font type B
            },
            "align": {
                "left": ESC + GS + b"a\x00",   # Left justification
                "center": ESC + GS + b"a\x01", # Centering
                "right": ESC + GS + b"a\x02",  # Right justification
            },
            "invert": {
                True: ESC + b"4",  # Inverse Printing ON
                False: ESC + b"5",  # Inverse Printing OFF
            },
            "color": {
                "black": ESC + b"\x72\x00",  # Default Color
                "red": ESC + b"\x72\x01",  # Alternative Color, Usually Red
            },
            "flip": {
                True: b"",  # Flip ON
                False: b"",  # Flip OFF
            },
            "density": {
                0: ESC + RS + b"d\x06",  # Printing Density -50%
                1: ESC + RS + b"d\x05",  # Printing Density -37.5%
                2: ESC + RS + b"d\x04",  # Printing Density -25%
                3: ESC + RS + b"d\x03",  # Printing Density -12.5%
                4: ESC + RS + b"d\x03",  # Printing Density  0%
                5: ESC + RS + b"d\x03",  # Printing Density +50%
                6: ESC + RS + b"d\x02",  # Printing Density +37.5%
                7: ESC + RS + b"d\x01",  # Printing Density +25%
                8: ESC + RS + b"d\x00",  # Printing Density +12.5%
            },
            "smooth": {
                True: b"",  # Smooth ON
                False: b"",  # Smooth OFF
            },
            "height": {  # Custom text height
                1: 0x00,
                2: 0x01,
                3: 0x02,
                4: 0x03,
                5: 0x04,
                6: 0x05,
                7: 0x06,
                8: 0x07,
            },
            "width": {  # Custom text width
                1: 0x00,
                2: 0x10,
                3: 0x20,
                4: 0x30,
                5: 0x40,
                6: 0x50,
                7: 0x60,
                8: 0x70,
            },
        }

        self.CODEPAGE_CHANGE = ESC + GS + b"\x74"

    def _cut_paper(self, full):
        return ESC + b'd' + b'\x02' if full else b'\x03'

    def set_codepage(self, page_num):
        return ESC + GS + b"\x74" + six.int2byte(page_num)

    def set_text_size(self, width, height):
        # not supported (?)
        return b""

    def set_font(self, n):
        return ESC + RS + b"F" + n

    def print_and_feed(self, n):
        """ print and feed n lines """
        return ESC + b"a" + six.int2byte(n)
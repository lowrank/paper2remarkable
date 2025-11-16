#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for arXiv provider

This file is part of paper2remarkable.

"""

import os
import re
import shutil
import tempfile
import unittest

from paper2remarkable.providers.arxiv import DEARXIV_TEXT_REGEX
from paper2remarkable.providers.arxiv import DEARXIV_URI_REGEX
from paper2remarkable.providers.arxiv import Arxiv


class TestArxiv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_dir = os.getcwd()

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_text_regex_1(self):
        key = b"arXiv:1908.03213v1 [astro.HE] 8 Aug 2019"
        m = re.fullmatch(DEARXIV_TEXT_REGEX, key)
        self.assertIsNotNone(m)

    def test_text_regex_2(self):
        key = b"arXiv:1908.03213v1 [astro-ph.HE] 8 Aug 2019"
        m = re.fullmatch(DEARXIV_TEXT_REGEX, key)
        self.assertIsNotNone(m)

    def test_text_regex_3(self):
        key = b"arXiv:physics/0605197v1  [physics.data-an]  23 May 2006"
        m = re.fullmatch(DEARXIV_TEXT_REGEX, key)
        self.assertIsNotNone(m)

    def test_text_regex_4(self):
        key = b"arXiv:math/0309285v2  [math.NA]  9 Apr 2004"
        m = re.fullmatch(DEARXIV_TEXT_REGEX, key)
        self.assertIsNotNone(m)

    def test_uri_regex_1(self):
        key = b"http://arxiv.org/abs/physics/0605197v1"
        m = re.fullmatch(DEARXIV_URI_REGEX, key)
        self.assertIsNotNone(m)

    def test_uri_regex_2(self):
        key = b"https://arxiv.org/abs/1101.0028v3"
        m = re.fullmatch(DEARXIV_URI_REGEX, key)
        self.assertIsNotNone(m)

    def test_stamp_removed_1(self):
        url = "https://arxiv.org/pdf/1703.06103.pdf"
        prov = Arxiv(upload=False)
        filename = prov.run(url, filename="./target.pdf")
        prov.uncompress_pdf(filename, "unc.pdf")
        with open("unc.pdf", "rb") as fp:
            data = fp.read()
        self.assertNotIn(b"arXiv:1703.06103v4  [stat.ML]  26 Oct 2017", data)

    def test_stamp_removed_2(self):
        url = "https://arxiv.org/abs/2003.06222"
        prov = Arxiv(upload=False)
        filename = prov.run(url, filename="./target.pdf")
        prov.uncompress_pdf(filename, "unc.pdf")
        with open("unc.pdf", "rb") as fp:
            data = fp.read()
        self.assertNotIn(b"arXiv:2003.06222v1  [stat.ML]  13 Mar 2020", data)

    def test_stamp_removed_3(self):
        url = "https://arxiv.org/abs/physics/0605197v1"
        prov = Arxiv(upload=False)
        filename = prov.run(url, filename="./target.pdf")
        prov.uncompress_pdf(filename, "unc.pdf")
        with open("unc.pdf", "rb") as fp:
            data = fp.read()
        self.assertNotIn(
            b"arXiv:physics/0605197v1  [physics.data-an]  23 May 2006", data
        )
        self.assertNotIn(
            b"/URI (http://arxiv.org/abs/physics/0605197v1)", data
        )

    def test_stamp_removed_4(self):
        url = "https://arxiv.org/abs/math/0309285v2"
        prov = Arxiv(upload=False)
        filename = prov.run(url, filename="./target.pdf")
        prov.uncompress_pdf(filename, "unc.pdf")
        with open("unc.pdf", "rb") as fp:
            data = fp.read()
        self.assertNotIn(b"arXiv:math/0309285v2  [math.NA]  9 Apr 2004", data)
        self.assertNotIn(b"/URI (http://arXiv.org/abs/math/0309285v2)", data)

    def test_stamp_removed_5(self):
        url = "https://arxiv.org/abs/astro-ph/9207001v1"
        prov = Arxiv(upload=False)
        filename = prov.run(url, filename="./target.pdf")
        prov.uncompress_pdf(filename, "unc.pdf")
        with open("unc.pdf", "rb") as fp:
            data = fp.read()
        self.assertNotIn(
            b"/URI (http://arxiv.org/abs/astro-ph/9207001v1)", data
        )

    def test_alphaxiv_validation_abs_1(self):
        url = "https://alphaxiv.org/abs/2003.06222"
        self.assertTrue(Arxiv.validate(url))

    def test_alphaxiv_validation_pdf_1(self):
        url = "https://alphaxiv.org/pdf/2003.06222.pdf"
        self.assertTrue(Arxiv.validate(url))

    def test_alphaxiv_validation_abs_2(self):
        url = "https://alphaxiv.org/abs/physics/0605197v1"
        self.assertTrue(Arxiv.validate(url))

    def test_alphaxiv_validation_pdf_2(self):
        url = "https://alphaxiv.org/pdf/physics/0605197v1.pdf"
        self.assertTrue(Arxiv.validate(url))

    def test_alphaxiv_to_arxiv_conversion(self):
        alphaxiv_url = "https://alphaxiv.org/abs/2003.06222"
        expected_arxiv_url = "https://arxiv.org/abs/2003.06222"
        self.assertEqual(
            Arxiv.convert_alphaxiv_to_arxiv(alphaxiv_url), expected_arxiv_url
        )

    def test_alphaxiv_get_abs_pdf_urls(self):
        alphaxiv_url = "https://alphaxiv.org/abs/2003.06222"
        prov = Arxiv(upload=False)
        abs_url, pdf_url = prov.get_abs_pdf_urls(alphaxiv_url)
        self.assertEqual(abs_url, "https://arxiv.org/abs/2003.06222")
        self.assertEqual(pdf_url, "https://arxiv.org/pdf/2003.06222.pdf")


if __name__ == "__main__":
    unittest.main()

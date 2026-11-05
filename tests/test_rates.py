import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_invalid_weight(self):
        for service in ("standard", "express"):
            for weight in (0, -1):
                with self.subTest(service=service, weight=weight):
                    with self.assertRaisesRegex(ValueError, "weight must be positive"):
                        shipping_quote(weight, "local", service=service)

    def test_explicit_standard_matches_default(self):
        for zone in ("local", "regional"):
            for weight in (0.5, 2, 3.141):
                with self.subTest(zone=zone, weight=weight):
                    expected = round((5 if zone == "local" else 8) + 1.5 * weight, 2)
                    self.assertEqual(shipping_quote(weight, zone), expected)
                    self.assertEqual(shipping_quote(weight, zone, "standard"), expected)

    def test_express_rates(self):
        for zone, expected in (("local", 15.0), ("regional", 18.0)):
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(2, zone, service="express"), expected)

    def test_express_fractional_weight(self):
        self.assertEqual(shipping_quote(3.141, "local", "express"), 16.71)
        self.assertEqual(shipping_quote(3.141, "regional", "express"), 19.71)

    def test_unknown_service(self):
        with self.assertRaisesRegex(ValueError, "unknown service"):
            shipping_quote(2, "local", service="overnight")

    def test_unknown_zone(self):
        for service in ("standard", "express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown zone"):
                    shipping_quote(2, "unknown", service=service)

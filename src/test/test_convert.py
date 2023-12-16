from convert import *
import unittest

class TestSum(unittest.TestCase):

    def test_bits_to_number(self):
        bits1 = '110010010101'
        bits2 = '0'
        bits3 = '11111111111111111111111111111111111111111111111111111111111111111'
        bits4 = '1200'
        bits5 = '0000000000000000000000000000000000000000000000000000000000000000'

        self.assertEqual(bits_to_number(bits1), 3221)
        self.assertEqual(bits_to_number(bits2), 0)
        self.assertEqual(bits_to_number(bits3), -1)
        self.assertEqual(bits_to_number(bits4), -1)
        self.assertEqual(bits_to_number(bits2), bits_to_number(bits5))

    def test_number_to_bits(self):
        number1 = 3221
        number2 = 0
        number3 = 18_446_744_073_709_551_616
        number4 = 18_446_744_073_709_551_615

        self.assertEqual(number_to_bits(number1), '0000000000000000000000000000000000000000000000000000110010010101')
        self.assertEqual(number_to_bits(number2), '0000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(number_to_bits(number3), -1)
        self.assertEqual(number_to_bits(number4), '1111111111111111111111111111111111111111111111111111111111111111')
        self.assertEqual(bits_to_number(number_to_bits(number1)), number1)

if __name__ == '__main__':
    unittest.main()
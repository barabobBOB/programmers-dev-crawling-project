import unittest
from cryto_apis_arch import CoinListDuplicateRemover


class TestCoinListDuplicateRemover(unittest.TestCase):
    def setUp(self):
        self.remover = CoinListDuplicateRemover()
        
    def test_get_krw_coins_from_upbit(self):
        coins = self.remover.get_krw_coins_from_upbit()
        self.assertIsInstance(coins, list)
        self.assertFalse(all([coin.endswith("KRW") for coin in coins]))
        
    def test_get_all_coins_from_bithumb(self):
        coins = self.remover.get_all_coins_from_bithumb()
        self.assertIsInstance(coins, list)
        self.assertFalse(all([coin.endswith("KRW") for coin in coins]))
        
    def test_get_all_coins_without_duplicate(self):
        coins = self.remover.get_all_coins_without_duplicate()
        self.assertIsInstance(coins, list)
        self.assertFalse(all([coin.endswith("KRW") for coin in coins]))
        self.assertEqual(len(coins), len(set(coins)))
        
if __name__ == "__main__":
    unittest.main()
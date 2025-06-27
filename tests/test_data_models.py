import os
import sys
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_path)
import unittest
from src.my_library.data_models import Token, Sentence, ModifiedToken, ModifiedSentence

class TestModifiedToken(unittest.TestCase):
    def setUp(self):
        token = Token("美しい", 1.0, "adjective", 1.0, 1.0, 2.0, 2.0)
        self.modified_token = ModifiedToken.modify_token(token)

    def test_calc_token_score(self):
        """calc_token_scoreメソッドのテスト"""
        self.assertEqual(self.modified_token.calc_token_score(), 4.0)

    def test_subtract(self):
        """subtractメソッドのテスト"""
        self.assertEqual(self.calc.subtract(5, 2), 3)
        self.assertEqual(self.calc.subtract(2, 5), -3)
        self.assertEqual(self.calc.subtract(10, 0), 10)

    def test_multiply(self):
        """multiplyメソッドのテスト"""
        self.assertEqual(self.calc.multiply(2, 3), 6)
        self.assertEqual(self.calc.multiply(-1, 5), -5)
        self.assertEqual(self.calc.multiply(0, 100), 0)

    def test_divide(self):
        """divideメソッドのテスト"""
        self.assertEqual(self.calc.divide(6, 2), 3.0)
        self.assertEqual(self.calc.divide(5, 2), 2.5)

    def test_divide_by_zero(self):
        """ゼロ除算のエラーハンドリングのテスト"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def tearDown(self):
        """各テストメソッドの実行後に呼び出されるクリーンアップ処理（オプション）"""
        # 必要であれば、ここでリソースの解放などを行う
        pass

if __name__ == '__main__':
    unittest.main()
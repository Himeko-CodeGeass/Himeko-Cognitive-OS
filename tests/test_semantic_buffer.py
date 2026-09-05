import unittest
from core.semantic_buffer import SemanticBuffer

class TestSemanticBuffer(unittest.TestCase):
    def test_initialization(self):
        buffer = SemanticBuffer(capacity=3)
        self.assertEqual(buffer.capacity, 3)
        self.assertEqual(len(buffer.get_context()), 0)

    def test_push_and_fifo(self):
        buffer = SemanticBuffer(capacity=2)
        buffer.push("msg1")
        buffer.push("msg2")
        self.assertEqual(buffer.get_context(), ["msg1", "msg2"])
        
        # 測試超過容量時的 FIFO 行為（最舊的 "msg1" 應該被擠出）
        buffer.push("msg3")
        self.assertEqual(buffer.get_context(), ["msg2", "msg3"])

    def test_clear(self):
        buffer = SemanticBuffer(capacity=3)
        buffer.push("test")
        buffer.clear()
        self.assertEqual(len(buffer.get_context()), 0)

if __name__ == '__main__':
    unittest.main()

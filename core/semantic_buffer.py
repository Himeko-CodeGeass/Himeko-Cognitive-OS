class SemanticBuffer:
    """Core Semantic Buffer for short-term context and memory caching."""
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.buffer = []

    def push(self, message):
        if not message:
            return False
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)  # 保持容量上限，移除最舊的記憶
        self.buffer.append(message)
        return True

    def get_context(self):
        return list(self.buffer)

    def clear(self):
        self.buffer.clear()

# -*- coding: utf-8 -*-
import os

try:
    from core.memory_manager import MemoryManager
    from core.tools import AgentTools
except ModuleNotFoundError:
    from .memory_manager import MemoryManager
    from .tools import AgentTools

class GestaltEngine:
    def __init__(self, db_path: str = "himeko_memory.db"):
        print("[GestaltEngine] Initializing...")
        self.memory = MemoryManager(db_path=db_path)
        self.tools = AgentTools()

    def process_intent(self, intent: str):
        print(f"[GestaltEngine] Processing intent: {intent}")
        history = self.memory.get_recent_history(limit=5)
        context_str = "\n".join([f"- [{m['role']}]: {m['content']}" for m in history])
        tool_result = None
        return {"status": "success", "context": context_str, "tool_result": tool_result}

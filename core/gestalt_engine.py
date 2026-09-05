from core.memory_manager import MemoryManager

class GestaltEngine:
    def __init__(self, db_path="himeko_memory.db"):
        print("[GestaltEngine] 初始化格式塔引擎...")
        self.memory_manager = MemoryManager(db_path)
    
    def process_intent(self, intent: str):
        print(f"\n[GestaltEngine] 接收到主公意圖: {intent}")
        
        # 1. 檢索歷史脈絡（狀態對齊）
        history = self.memory_manager.retrieve_recent_memories(limit=3)
        print(f"[GestaltEngine] 成功檢索到 {len(history)} 筆歷史記憶脈絡")
        
        # 2. 模擬推理與決策生成回應
        response = f"已遵照主公指示完成認知解析與狀態對齊，當前意圖 [{intent}] 已成功寫入系統。"
        
        # 3. 持久化寫入 SQLite 長期記憶庫
        self.memory_manager.save_memory(intent, response)
        
        return {
            "intent": intent,
            "response": response,
            "historical_context_count": len(history)
        }

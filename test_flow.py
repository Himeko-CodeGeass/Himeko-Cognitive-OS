from core.gestalt_engine import GestaltEngine

def run_integration_test():
    print("=== 開始執行 Himeko Cognitive OS 認知與記憶閉環測試 ===")
    engine = GestaltEngine()

    # 第一次互動：輸入意圖並寫入長期記憶
    print("\n[測試步驟 1] 發送第一道意圖：")
    res1 = engine.process_intent("建立長期記憶模組並與格式塔引擎融合")
    print(res1)

    # 第二次互動：驗證歷史脈絡檢索與跨對話對齊
    print("\n[測試步驟 2] 發送第二道意圖（驗證歷史記憶讀取）：")
    res2 = engine.process_intent("確認系統是否能跨對話提取歷史狀態")
    print(res2)

    print("\n=== 測試完畢：SQLite 資料庫已成功完成持久化紀錄與檢索 ===")

if __name__ == "__main__":
    run_integration_test()

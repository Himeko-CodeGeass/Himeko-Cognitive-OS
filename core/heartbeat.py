import time
import datetime
from core.gestalt_engine import GestaltEngine

class HeartbeatEngine:
    def __init__(self, engine: GestaltEngine, interval_seconds: int = 5):
        self.engine = engine
        self.interval_seconds = interval_seconds
        self.is_running = False

    def pulse(self, adapter=None):
        timestamp = datetime.datetime.now().isoformat()
        intent = f"[HEARTBEAT_PULSE] System self-check at {timestamp}"
        print(f"\n[Heartbeat] ❤️ Thumping... {timestamp}")
        
        result = self.engine.process_intent(intent, adapter=adapter)
        print(f"[Heartbeat] 🧠 Thought generated: {result['response']}")
        return result

    def start_loop(self, count: int = 3, adapter=None):
        print(f"[Heartbeat] Starting autonomous heartbeat loop (Interval: {self.interval_seconds}s, Pulses: {count})...")
        self.is_running = True
        
        for i in range(count):
            if not self.is_running:
                break
            print(f"--- Pulse {i+1}/{count} ---")
            self.pulse(adapter=adapter)
            if i < count - 1:
                time.sleep(self.interval_seconds)
                
        print("[Heartbeat] Loop completed.")

    def stop_loop(self):
        self.is_running = False
        print("[Heartbeat] Stopped.")

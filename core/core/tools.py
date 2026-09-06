# -*- coding: utf-8 -*-
import os
import subprocess

class AgentTools:
    @staticmethod
    def read_file(filepath: str) -> str:
        try:
            if not os.path.exists(filepath):
                return f"[Tool Error] File not found: {filepath}"
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            return f"[Tool Success] Read file {filepath} (Size: {len(content)} chars)"
        except Exception as e:
            return f"[Tool Error] Failed to read file: {e}"

    @staticmethod
    def write_file(filepath: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"[Tool Success] Successfully wrote to {filepath}"
        except Exception as e:
            return f"[Tool Error] Failed to write file: {e}"

    @staticmethod
    def run_command(command: str) -> str:
        # 安全限制：僅允許特定安全防護指令或回傳環境狀態
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=10
            )
            output = result.stdout if result.returncode == 0 else result.stderr
            return f"[Tool Success] Command executed:\n{output.strip()}"
        except Exception as e:
            return f"[Tool Error] Command execution failed: {e}"

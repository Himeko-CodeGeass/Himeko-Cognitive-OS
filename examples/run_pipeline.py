"""
Himeko-Cognitive-OS: Integration Pipeline Demo v1.0
Author: Himeko-CodeGeass (主公)
Description: Integrates Gestalt Engine, Semantic Buffer, and Dynamic Constitution into a unified workflow.
"""

import sys
import os

# Add parent directory to path to resolve core imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from core.gestalt_engine.engine import GestaltEngine
from core.semantic_buffer.buffer import SemanticBufferLayer
from core.dynamic_constitution.constitution import DynamicConstitution

def run_cognitive_pipeline():
    print("=" * 60)
    print(" HIMEKO-COGNITIVE-OS: FULL PIPELINE EXECUTION STARTED")
    print("=" * 60)

    # 1. Initialize Modules
    gestalt = GestaltEngine(sensitivity_threshold=0.6)
    buffer = SemanticBufferLayer(friction_tolerance=0.4)
    constitution = DynamicConstitution()

    # 2. Simulate Incoming Human-AI Interaction Data
    raw_input = "Refactoring legacy architecture under heavy deadline pressure."
    metadata = {"pause_count": 2, "revision_count": 3}
    emotional_weight = 0.55
    adversarial_score = 0.8

    print(f"\n[Input Stream]: {raw_input}")

    # 3. Step A: Semantic Buffer Decoupling
    buffer_result = buffer.decouple_intent(raw_input, emotional_weight)
    print(f"-> [Semantic Buffer]: {buffer_result['status']}")

    # 4. Step B: Gestalt Engine Intent Distillation
    exhaust_result = gestalt.distill_digital_exhaust(raw_input, metadata)
    skeleton = gestalt.generate_semantic_skeleton("Modular System Refactoring")
    print(f"-> [Gestalt Engine]: Friction Index = {exhaust_result['friction_index']}")
    print(f"-> {skeleton}")

    # 5. Step C: Dynamic Constitution Evaluation
    const_result = constitution.evaluate_adversarial_input(adversarial_score)
    print(f"-> [Dynamic Constitution]: {const_result['status']}")
    print(f"-> Current Protocol Version: {const_result['current_version']}")

    print("\n" + "=" * 60)
    print(" PIPELINE EXECUTION COMPLETE: SYSTEM NOMINAL")
    print("=" * 60)

if __name__ == "__main__":
    run_cognitive_pipeline()

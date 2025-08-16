"""Debug imports to find the issue."""
import sys
import os

print("Python path:")
for p in sys.path:
    print(f"  {p}")

print("\nTrying to find langgraph_agent_lib:")
try:
    import langgraph_agent_lib
    print(f"Found at: {langgraph_agent_lib.__file__}")
    print(f"Contains: {dir(langgraph_agent_lib)}")
except ImportError as e:
    print(f"Import error: {e}")

print("\nTrying to find models.py:")
models_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                          "langgraph_agent_lib", "models.py")
print(f"Looking for: {models_path}")
print(f"File exists: {os.path.exists(models_path)}")

if os.path.exists(models_path):
    print("\nContents of models.py:")
    with open(models_path, 'r') as f:
        print(f.read())

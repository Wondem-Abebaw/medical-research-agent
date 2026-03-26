"""
Visualize the Medical Research Agent workflow
"""
import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app.agents.graph import MedicalResearchAgent

def generate_diagram():
    """Generate and save workflow diagram"""
    
    print("Creating Medical Research Agent...")
    agent = MedicalResearchAgent()
    
    print("Generating diagram...")
    
    # Option 1: Save as PNG
    try:
        png_data = agent.graph.get_graph().draw_mermaid_png()
        
        with open("workflow_diagram.png", "wb") as f:
            f.write(png_data)
        
        print("✅ PNG diagram saved: workflow_diagram.png")
    except Exception as e:
        print(f"❌ PNG generation failed: {e}")
    
    # Option 2: Save as Mermaid text (can paste into mermaid.live)
    try:
        mermaid_text = agent.graph.get_graph().draw_mermaid()
        
        with open("workflow_diagram.mmd", "w") as f:
            f.write(mermaid_text)
        
        print("✅ Mermaid text saved: workflow_diagram.mmd")
        print("   View at: https://mermaid.live")
    except Exception as e:
        print(f"❌ Mermaid text generation failed: {e}")
    
    # Option 3: Print ASCII representation
    try:
        print("\n" + "="*60)
        print("ASCII Representation:")
        print("="*60)
        print(agent.graph.get_graph().draw_ascii())
    except Exception as e:
        print(f"❌ ASCII generation failed: {e}")

if __name__ == "__main__":
    generate_diagram()
#!/usr/bin/env python3
"""
Resume paused project automation.

This script safely resumes a paused project by updating the state
without shell escaping issues.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir))

# Also try to add the src directory if we're in a different structure
src_dir = script_dir / 'src'
if src_dir.exists():
    sys.path.insert(0, str(src_dir))

try:
    from state_manager import StateManager
except ImportError:
    # Try alternative import path
    try:
        from src.state_manager import StateManager
    except ImportError:
        print("❌ Error: Unable to import StateManager. Check project structure.")
        sys.exit(1)


def main():
    """Resume paused project."""
    try:
        # Initialize StateManager
        sm = StateManager('.')
        
        # Read current state
        state = sm.read()
        
        # Check if project is paused
        if state.get('status') != 'paused':
            print(f"❌ Error: Project is not paused (status: {state.get('status')})")
            sys.exit(1)
        
        # Display resume information
        workflow_step = state.get('workflow_step', 'unknown')
        current_sprint = state.get('current_sprint', 'unknown')
        print(f"Resuming from: {workflow_step} step in sprint {current_sprint}")
        
        # Update state to resume
        sm.update({
            'status': 'active',
            'automation_active': True,
            'pause_reason': None,
            'paused_at': None
        })
        
        print("✅ Project resumed successfully")
        
    except FileNotFoundError:
        print("❌ Error: No project state found. Not in a project directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
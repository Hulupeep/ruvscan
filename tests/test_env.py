#!/usr/bin/env python3
"""Quick environment verification test"""
import os
from pathlib import Path

def test_env():
    """Check if .env.local has required variables"""
    env_file = Path(".env.local")
    
    if not env_file.exists():
        print("❌ .env.local not found")
        return False
    
    # Read .env.local
    env_vars = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    # Check required variables
    required = ['GITHUB_TOKEN', 'OPENAI_API_KEY']
    missing = []
    
    for var in required:
        if var not in env_vars:
            missing.append(var)
        else:
            # Show masked value
            value = env_vars[var]
            if value:
                masked = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
                print(f"✅ {var}: {masked}")
            else:
                missing.append(f"{var} (empty)")
    
    if missing:
        print(f"\n❌ Missing or empty: {', '.join(missing)}")
        return False
    
    print("\n✅ All required environment variables set!")
    return True

if __name__ == "__main__":
    test_env()

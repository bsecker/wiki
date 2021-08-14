"""
functions for setting up seckerwiki
"""
import os


EXAMPLE_CONTENTS = """---
journal-path: Personal/Personal/Management/Journal
"""

def setup():
  path = os.path.join(os.getcwd(), "wiki.yml")

  if os.path.exists(path):
    print(f"Error: seckerwiki config file already exists at {path}")
    return False
    
  with open(path, 'w') as f:
      f.write(EXAMPLE_CONTENTS)
  os.chmod(path,0o600)

  print(f"Configuration file written to {path}")
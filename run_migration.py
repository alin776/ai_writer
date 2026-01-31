import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Run alembic upgrade
os.chdir('backend')
os.system('alembic upgrade head')

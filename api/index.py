import sys
import os
from pathlib import Path

# Ensure the api directory is in the path
sys.path.insert(0, str(Path(__file__).parent))

from mangum import Mangum
from main import app

handler = Mangum(app)

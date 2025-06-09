import sys
import os

print("Python path:", sys.path)
print("Current directory:", os.getcwd())

try:
    import ventai
    print("Successfully imported ventai package")
    print("Package location:", ventai.__file__)
    
    from ventai.backend.main import app
    print("Successfully imported app from ventai.backend.main")
    
    print("Import test passed successfully")
except Exception as e:
    print(f"Import failed: {str(e)}")
    raise

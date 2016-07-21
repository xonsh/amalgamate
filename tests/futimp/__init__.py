# amalgamate
import os as _os
if _os.getenv('DEBUG', ''):
    pass
else:
    import sys as _sys
    try:
        from futimp import __amalgam__
        x = __amalgam__
        _sys.modules['futimp.x'] = __amalgam__
        y = __amalgam__
        _sys.modules['futimp.y'] = __amalgam__
        del __amalgam__
    except ImportError:
        pass
    del _sys
del _os
# amalgamate end

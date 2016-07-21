def a():
    pass

# amalgamate
import os as _os
if _os.getenv('DEBUG', ''):
    pass
else:
    import sys as _sys
    try:
        from relimp import __amalgam__
        x = __amalgam__
        _sys.modules['relimp.x'] = __amalgam__
        y = __amalgam__
        _sys.modules['relimp.y'] = __amalgam__
        del __amalgam__
    except ImportError:
        pass
    del _sys
del _os
# amalgamate end

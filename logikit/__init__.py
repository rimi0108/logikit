"""
Logikit - Automatically visualize function execution with Python decorator

Usage:
    from logikit import logikit

    @logikit(condition_map={
        "_fails_regulated_area_rules": "Check regulated area requirements",
        "_fails_public_housing_zone_rules": "Check public housing zone requirements",
    })
    def is_eligible(self):
        if self._fails_regulated_area_rules():
            return False
        if self._fails_public_housing_zone_rules():
            return False
        return True
"""

# Import decorator - use relative import
from .decorator import logikit

# Import trace classes and functions - use relative import
from .trace import TraceStep
from .trace import generate_flowchart_from_trace

__version__ = "0.1.0"

# Explicitly make available at package level
__all__ = ["logikit", "TraceStep", "generate_flowchart_from_trace"]

# Logikit

Automatically trace function execution and generate flowcharts with a Python decorator

## Installation

### Local Installation (Development)

From the project root:

```bash
cd logikit
pip install -e .
```

Or directly from the project root:

```bash
pip install -e ./logikit
```

### PyPI Distribution (Future)

```bash
pip install logikit
```

## Usage

### Basic Usage

```python
from logikit import logikit

class MyChecker:
    @logikit(condition_map={
        "_fails_regulated_area_rules": "Check regulated area requirements",
        "_fails_public_housing_zone_rules": "Check public housing zone requirements",
        "_has_invalid_account": "Check account validity",
    })
    def is_eligible(self):
        if self._fails_regulated_area_rules():
            return False
        if self._fails_public_housing_zone_rules():
            return False
        if self._has_invalid_account():
            return False
        return True

    def _fails_regulated_area_rules(self):
        # Actual condition check logic
        return False

    def _fails_public_housing_zone_rules(self):
        return False

    def _has_invalid_account(self):
        return False
```

### Accessing Trace

After function execution, you can access the trace from the instance's `_logikit_trace` attribute:

```python
checker = MyChecker()
result = checker.is_eligible()

# Access trace
trace = checker._logikit_trace
for step in trace:
    print(f"{step.label}: {'PASS' if step.passed else 'FAIL'}")
```

### Generating Flowcharts

```python
from logikit import generate_flowchart_from_trace

checker = MyChecker()
result = checker.is_eligible()

# Generate Mermaid flowchart code
mermaid_code = generate_flowchart_from_trace(checker._logikit_trace)
print(mermaid_code)
```

## How It Works

1. The `@logikit` decorator parses the function's source code to identify the order of conditional statements.
2. During function execution, each condition is evaluated sequentially and results are traced.
3. The trace is stored in the instance's `_logikit_trace` attribute.
4. You can generate Mermaid flowchart code using the `generate_flowchart_from_trace()` function.

## License

MIT

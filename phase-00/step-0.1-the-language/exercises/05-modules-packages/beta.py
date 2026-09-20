"""The other half of the cycle. Runs while alpha is still half-built."""

import alpha

B_VALUE = "b"

# Read at module level, so it captures alpha's state mid-import.
saw_a_value = hasattr(alpha, "A_VALUE")

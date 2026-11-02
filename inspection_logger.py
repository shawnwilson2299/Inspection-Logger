"""Verdict rules for the Inspection Defect Logger."""

# Each row is (minimum sample size, major limit, minor limit).
ACCEPTANCE_LIMITS = (
    (1, 0, 1),
    (12, 1, 3),
    (45, 3, 7),
    (160, 6, 14),
    (650, 12, 28),
)
SEVERITIES = ("critical", "major", "minor")


def acceptance_limits(sample_size: int) -> tuple[int, int]:
    """Return the major and minor limits for a valid sample size."""
    if isinstance(sample_size, bool) or not isinstance(sample_size, int):
        raise ValueError("Sample size must be a whole number of at least 1.")
    if sample_size < 1:
        raise ValueError("Sample size must be at least 1.")

    for minimum, major_limit, minor_limit in reversed(ACCEPTANCE_LIMITS):
        if sample_size >= minimum:
            return major_limit, minor_limit

    # The first row starts at 1, so valid sizes always return from the loop.
    raise ValueError("No acceptance limits are defined for this sample size.")


def verdict_for(sample_size: int, defects: list[dict[str, str]]) -> str:
    """Calculate ACCEPT or REJECT from the sample size and recorded defects."""
    major_limit, minor_limit = acceptance_limits(sample_size)
    counts = {severity: 0 for severity in SEVERITIES}
    for defect in defects:
        severity = defect["severity"]
        if severity not in counts:
            raise ValueError(f"Unknown defect severity: {severity}")
        counts[severity] += 1

    if (
        counts["critical"] >= 1
        or counts["major"] > major_limit
        or counts["minor"] > minor_limit
    ):
        return "REJECT"
    return "ACCEPT"


def main() -> None:
    print("Inspection Defect Logger")
    print("The command-line interface is in progress.")


if __name__ == "__main__":
    main()

"""Interactive CLI and verdict rules for the Inspection Defect Logger."""

from dataclasses import dataclass, field

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


@dataclass
class Inspection:
    """One inspection and the defects recorded during the current run."""

    batch_id: str
    sample_size: int
    defects: list[dict[str, str]] = field(default_factory=list)

    def record_defect(self, severity: str, description: str) -> None:
        severity = severity.strip().lower()
        description = description.strip()
        if severity not in SEVERITIES:
            raise ValueError("Severity must be critical, major, or minor.")
        if not description:
            raise ValueError("Description cannot be empty.")
        self.defects.append({"severity": severity, "description": description})

    def verdict(self) -> str:
        return verdict_for(self.sample_size, self.defects)


def ask_for_sample_size() -> int:
    while True:
        raw = input("Sample size (whole number, at least 1): ").strip()
        try:
            size = int(raw)
            acceptance_limits(size)
            return size
        except ValueError as error:
            print(f"Invalid sample size: {error}")


def start_inspection() -> Inspection:
    print("Inspection Defect Logger")
    while True:
        batch_id = input("Batch ID: ").strip()
        if batch_id:
            break
        print("Batch ID cannot be empty.")
    sample_size = ask_for_sample_size()
    return Inspection(batch_id=batch_id, sample_size=sample_size)


def show_defects(inspection: Inspection) -> None:
    if not inspection.defects:
        print("No defects recorded.")
        return
    print(f"Defects for batch {inspection.batch_id}:")
    for number, defect in enumerate(inspection.defects, start=1):
        print(f"{number}. {defect['severity'].capitalize()}: {defect['description']}")


def main() -> None:
    inspection = start_inspection()
    print(f"Inspection started for batch {inspection.batch_id} (sample size {inspection.sample_size}).")
    print("Commands: record, list, verdict, quit")

    while True:
        command = input("\n> ").strip().lower()
        if command == "record":
            severity = input("Severity (critical / major / minor): ").strip().lower()
            description = input("Short description: ").strip()
            try:
                inspection.record_defect(severity, description)
                print("Defect recorded.")
            except ValueError as error:
                print(f"Invalid defect: {error}")
        elif command == "list":
            show_defects(inspection)
        elif command == "verdict":
            print(f"Verdict for batch {inspection.batch_id}: {inspection.verdict()}")
        elif command in {"quit", "exit"}:
            print("Inspection ended. Recorded data was only held in memory for this run.")
            break
        else:
            print("Unknown command. Choose record, list, verdict, or quit.")


if __name__ == "__main__":
    main()

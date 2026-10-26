"""NX entry point for the model checker."""
from check_runner import CheckRunner


def main():
    runner = CheckRunner.from_active_nx_part()
    results = runner.run()
    report = runner.build_report(results)

    # Keep the NX entry point deliberately small. UI, REST upload and automatic
    # fixes can later consume the same report without changing the checks.
    print("NX Model Check:", report["status"])
    for result in results:
        print(f"[{result.status.value}] {result.rule_id}: {result.message}")

    return report


if __name__ == "__main__":
    main()

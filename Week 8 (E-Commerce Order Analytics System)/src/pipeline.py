"""Run the complete generate-clean-load-analyze pipeline."""
from .generate_data import generate_data
from .cleaning import clean_and_validate
from .database import build_database, run_analyses


def main() -> None:
    counts = generate_data()
    quality = clean_and_validate()
    db = build_database()
    reports = run_analyses()
    print(f"Generated: {counts}")
    print(f"Data quality report: {quality}")
    print(f"Database: {db}")
    print(f"SQL reports created: {len(reports)}")


if __name__ == "__main__":
    main()

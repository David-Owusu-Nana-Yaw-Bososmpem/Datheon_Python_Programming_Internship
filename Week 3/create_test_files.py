"""Create extension-based sample files for testing the directory organizer."""

from pathlib import Path

TEST_FOLDER = Path("organizer_test")

SAMPLES = {
    "example.py": "print('Hello from Python')\n",
    "sample_report.pdf": "Placeholder file for extension-classification testing.\n",
    "sales_data.xlsx": "Placeholder file for extension-classification testing.\n",
    "profile.jpg": "Placeholder file for extension-classification testing.\n",
    "meeting_notes.txt": "These are sample meeting notes.\n",
    "monthly_data.csv": "month,total\nJanuary,120\nFebruary,135\n",
}

def main():
    TEST_FOLDER.mkdir(exist_ok=True)
    print(f"Creating sample files in: {TEST_FOLDER.resolve()}")
    for filename, content in SAMPLES.items():
        path = TEST_FOLDER / filename
        if path.exists():
            print(f"Skipped (already exists): {filename}")
            continue
        path.write_text(content, encoding="utf-8")
        print(f"Created: {filename}")

    print("\nSample files are ready.")
    print("NOTE: PDF, XLSX, and JPG samples are placeholders. They test")
    print("extension-based sorting, not whether those files open correctly.")

if __name__ == "__main__":
    main()

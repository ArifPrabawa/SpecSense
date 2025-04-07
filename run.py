"""
CLI stub for SpecSense.

Eventually this will:
- Accept a file path
- Parse it using the structured parser
- Display results or send them to an LLM for analysis
"""

from app.parser import parse_sections_with_bodies

def main():
    print("SpecSense CLI placeholder")
    sample = """# Test Section
This is a placeholder SRS block.
"""
    output = parse_sections_with_bodies(sample)
    for section in output:
        print(f"== {section['title']} ==")
        print(section['body'])
        print()

if __name__ == "__main__":
    main()

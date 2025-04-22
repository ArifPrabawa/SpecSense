import json
import csv
import io


def build_traceability_index(sections: list[dict]) -> dict:
    """
    Builds a mapping of requirement ID → section context and original text line.
    """
    index = {}

    for section in sections:
        for requirement in section.get("requirements", []):
            index[requirement["id"]] = {
                "section_id": section["id"],
                "section_title": section["title"],
                "text": requirement["text"],
            }

    return index


def export_traceability_as_json(index: dict) -> str:
    """
    Serializes the traceability index as a formatted JSON string.
    """
    return json.dumps(index, indent=2)


def export_traceability_as_csv(index: dict) -> str:
    """
    Converts the traceability index into a CSV string suitable for download.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Write CSV header
    writer.writerow(["requirement_id", "section_id", "section_title", "text"])

    # Write one row per requirement
    for req_id, data in index.items():
        writer.writerow(
            [
                req_id,
                data.get("section_id", ""),
                data.get("section_title", ""),
                data.get("text", ""),
            ]
        )

    # Return the complete CSV content as a string
    return output.getvalue()

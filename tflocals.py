import argparse
import re


def extract_outermost_content(source_code: str) -> str:
    """Extract the outermost content between curly braces."""
    stack = []
    outermost_content = ""
    inside_braces = False

    for char in source_code:
        if char == "{":
            stack.append(char)
            if not inside_braces:
                inside_braces = True
                continue
        elif char == "}" and stack:
            stack.pop()
            if not stack:
                inside_braces = False
                # continue
                break

        if inside_braces:
            outermost_content += char

    return outermost_content


def get_locals(file_path: str) -> str:
    """Extract locals blocks from a terraform HCL."""
    locals = ""
    try:
        with open(file_path, "r") as file:
            source_code = file.read()
            for match in re.finditer("locals ", source_code):
                # Remove the beginning of the file up to the first occurrence of "locals"
                locals_beginning = source_code[match.start() :]
                content = extract_outermost_content(locals_beginning)
                locals = f"locals {{ {content}\n}}"
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return locals


def replace_data_sources_with_strings(source_code: str) -> str:
    """Replace all the variables that refer to 'data' with a string."""
    pattern = re.compile(r"\bdata\.[a-zA-Z0-9_.]*")
    matches = pattern.finditer(source_code)
    modified_text = ""
    prev_end = 0
    for match in matches:
        start, end = match.start(), match.end()
        modified_text += (
            source_code[prev_end:start] + f'"FIXME_REPLACED_{source_code[start:end]}"'
        )  # Replace with an empty string
        prev_end = end
    modified_text += source_code[
        prev_end:
    ]  # Append the remaining part of the source code

    return modified_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="tflocals",
        description="Extract locals blocks from a terraform HCL file and replace data sources with strings.",
        epilog="Example: python tflocals.py /path/to/file.tf",
    )
    parser.add_argument("filepath", help="The path to the .tf file")
    args = parser.parse_args()
    locals = get_locals(args.filepath)
    src = replace_data_sources_with_strings(locals)
    print(src)

import pathlib
import re

# Suspicious dbt/Terraform patterns
PATTERNS = [
    r"{{\s*config\(.*?\)}}",
    r"{{\s*ref\(.*?\)}}",
    r"{{\s*var\(.*?\)}}",
    r"{{\s*env_var\(.*?\)}}",
    r"{{\s*target\..*?}}",
]

# Regex for code fences (triple backticks with optional language)
CODE_BLOCK_RE = re.compile(r"(```[a-zA-Z0-9_-]*\n.*?\n```)", re.DOTALL)

def wrap_raw_in_block(block: str) -> str:
    """Wrap dbt/Terraform {{ ... }} inside {% raw %}...{% endraw %}."""
    for pat in PATTERNS:
        block = re.sub(
            pat,
            lambda m: "{% raw %}" + m.group(0) + "{% endraw %}",
            block,
        )
    return block

def process_content(content: str) -> str:
    """Only wrap inside triple backtick code fences."""
    def replacer(match):
        return wrap_raw_in_block(match.group(1))

    return CODE_BLOCK_RE.sub(replacer, content)

def main():
    templates_dir = pathlib.Path("templates")
    for tpl in templates_dir.rglob("*.jinja2"):
        original = tpl.read_text(encoding="utf-8")
        updated = process_content(original)

        if updated != original:
            print(f"✅ Wrapped raw blocks in: {tpl}")
            tpl.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    main()

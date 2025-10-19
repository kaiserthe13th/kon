# KON — Kaiserthe13th's Object Notation

A small, human-friendly object notation and parser library. KON aims to be easy to read and write by humans while remaining straightforward to parse and emit from programs. This repository contains a lightweight Python implementation for parsing and dumping KON data.

The README below gives a short guide to the format, a few quick examples, and contribution guidelines for proposing and implementing new features.

## 📝 Quick format guide

KON is an object notation similar in spirit to JSON or INI but with a concise, developer-friendly syntax.

Basic rules:

- Objects use either braces or implicit form:

```ini
person {
    name = "Alice"
    age = 30
}
# Same as
# {person = {name = "Alice", age = 30}}

# The implicit form can be used for the following as well:
my little pony = MLP
# which is equivalent to
{my = {little = {pony = "MLP"}}}
```

- Key/value pairs are written as `key = value`. Values may be:
  - Strings (quoted with single or double quotes)
  - Unquoted identifiers (alphanumeric and underscore or one of `S-:` (for `-` it is only when non-leading)) which may represent
  - A few keywords exist, which cannot be used as strings: `true` / `false` (for booleans), (`inf`, `Inf`, `infinity`, `Infinity`, `nan`, `Nan`, `NaN`) for special floating point numbers
  - Numbers (integers or floats)
  - Arrays/lists using parentheses `(...)`
  - Nested objects using braces `{...}` or an implicit as shown above

- Lists are comma or newline separated and use parentheses in KON:

```ini
colors(red, green, blue)
# The above syntax is equivalent to
# colors = (red, green, blue)
items(
    { id = Open }
    { id = Save }
)
```

- Common keywords: `true`, `false`, and `null` map to Python's `True`, `False`, and `None`.

- Strings support standard backslash escapes (\n, \t, \\) and multi-line strings with a leading `|` marker. Multi-line strings will be dedented automatically when using the `|` marker.

Examples (JSON vs KON):

```json
{
    "widget": {
        "debug": "on",
        "window": {
            "title": "Sample Konfabulator Widget",
            "name": "main_window",
            "width": 500,
            "height": 500
        }
    }
}
```

```ini
widget {
    debug = on
    window {
        title = "Sample Konfabulator Widget"
        name = main_window
        width = 500
        height = 500
    }
}
```

## 🧵 Strings and multiline strings

- Single-line strings: either "double quoted" or 'single quoted'.
- Multi-line strings:
  - By default the behaviour is to not do anything to the string and keep it whatever way it was given
    (`MultilineStringBehaviour.IGNORE`). But this can be updated to error on multiline strings
    (`MultilineStringBehaviour.VALUE_ERROR`) or prefer dedenting (`MultilineStringBehaviour.DEDENT`).
  - Prefix with `<` immediately before the opening quote to enable dedenting (of the final string, after escapes are processed).
  - Prefix with `|` immediately before the opening quote to ensure that the string is not touched and allowed.

```ini
# The first newline (if exists), is removed
message = <"
    Hello world
    This is a dedented multi-line string"
# Everything is preserved, to ignore the newline, notice the explicit escape
message2 = |"\
  But this
    ain't getting
  dedented"
```

When using the `|` marker the implementation will remove common indentation from all non-empty lines.

## 🔎 Small reference

- Booleans: `true` / `false`
- Null: `null`
- Numbers: integers (e.g. `42`) and floats (e.g. `3.14`, `inf`, `nan`)
- Lists: `(a, b, c)`
- Objects: `{ key = value }` or the implicit form described above

## 🤝 Contribution guidelines

We welcome contributions. To keep the project organized we require feature proposals to follow a simple issue-based process. Small fixes and documentation improvements may be submitted as pull requests directly.

Feature proposal workflow

1. Open a new issue in this repository with both the `proposal` and `feat` labels.
2. Use the proposal template below in the issue body. Provide an example usage and clearly explain the use case.
3. If you have an implementation already available in your fork, include a link to the branch or PR in your fork. If no implementation exists, that's fine — proposals without implementations are accepted for discussion.
4. The maintainers will discuss the proposal, may request changes, and leave a status update in the issue. Once a proposal is accepted, create a draft PR that references the issue. The PR should include tests demonstrating the feature and documentation updates.

Proposal template (copy into your issue):

```text
Title: Short descriptive title

Summary:
- One-paragraph description of the feature

Motivation / Use case:
- Why is this feature useful? Who benefits?

Example usage:
- Minimal KON example showing the new syntax and sample data

Syntax notes:
- Should this be enabled by default or behind an option? (toggleable: yes/no)
- Describe how the syntax is distinguished (e.g., special marker, new keyword, or alternate container)

Backward compatibility:
- Any potential conflicts with existing KON documents?

Implementation (optional):
- Link to a fork/branch with an implementation, if available
- List of files or modules you modified (if you implemented it)

Tests:
- What tests would you add to `tests/` to validate behavior?

Other notes:
- Any performance/security/validation concerns
```

Labeling and tags

- When you open the proposal issue, please tag it with `proposal` and `feat`. This helps maintainers triage and track feature discussions.

When to open a direct Pull Request

- Bug fixes, small improvements, and documentation updates that do not change the KON syntax or add major features may be submitted as PRs directly. For syntax/feature changes, always start with an issue following the proposal template above.

## 🚀 Getting started

### Testing

Create a virtual environment and run the test suite with uv (take a look at [tests/README.md](tests/README.md))

## License ⚖️

See the repository license file for license details.

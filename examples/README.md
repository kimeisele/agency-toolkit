# Examples

This directory contains example files for using Agency Toolkit.

## Social Posts CSV (`social_posts.csv`)

Example CSV for batch generating social media posts.

**Usage:**
```bash
agency-toolkit social batch social_posts.csv --output ./output
```

**Format:**
- `text` - Post text content
- `style` - Visual style (modern, minimal, bold)
- `color` - Text color (hex format)
- `background` - Background color (hex format)

---

## Briefings CSV (`briefings.csv`)

Example CSV for batch generating project briefings.

**Usage:**
```bash
agency-toolkit briefing batch briefings.csv --output ./output --format markdown
```

**Format:**
- `client_name` - Client company name
- `project_name` - Project name
- `project_type` - Type of project (Web Development, Branding, Marketing, etc.)
- `goals` - Project goals (pipe-separated: `Goal 1|Goal 2|Goal 3`)
- `target_audience` - Target audience description
- `timeline` - Project timeline
- `budget` - Budget amount
- `deliverables` - Deliverables list (pipe-separated: `Item 1|Item 2|Item 3`)
- `additional_notes` - Additional notes (optional)

---

## Tips

1. **Pipe Separation**: Use `|` (pipe) to separate list items in CSV fields like goals and deliverables
2. **Quotes**: Wrap text containing commas in quotes
3. **Colors**: Use hex format for colors (e.g., `#000000` for black)
4. **File Paths**: Use relative or absolute paths for output directories

---

## Python API Examples

### Generate Social Post

```python
from extensions.social_posts import generate_social_post

post = generate_social_post(
    text="Hello World!",
    style="modern",
    color="#000000",
    background="#FFFFFF",
    output_dir="./output"
)

print(f"Generated post: {post.id}")
```

### Generate Briefing

```python
from extensions.briefing_generator import generate_briefing, BriefingData

data = BriefingData(
    client_name="Acme Corp",
    project_name="Website Redesign",
    project_type="Web Development",
    goals=["Increase conversions", "Improve UX"],
    target_audience="B2B decision makers",
    timeline="3 months",
    budget="$50,000",
    deliverables=["Wireframes", "Designs", "Development"]
)

briefing = generate_briefing(data, output_dir="./output", format="markdown")
print(f"Generated briefing: {briefing.id}")
```

### Generate Folder Structure

```python
from extensions.folder_structure import generate_folder_structure

structure = generate_folder_structure(
    project_name="My Awesome Project",
    structure_type="agency_standard",
    base_path="./projects"
)

print(f"Created structure at: {structure.metadata['project_root']}")
```

### Batch Processing

```python
from extensions.social_posts import batch_generate_social_posts
from pathlib import Path

assets = batch_generate_social_posts(
    csv_path=Path("social_posts.csv"),
    output_dir=Path("./output")
)

print(f"Generated {len(assets)} social posts")
```

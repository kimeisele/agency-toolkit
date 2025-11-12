# Agency Toolkit

**Professional automation for agencies** - Built on Genesis Core architecture.

## Architecture: Genesis Core Approach

This project follows the **Genesis Core** design pattern:

- **8 Frozen Core Modules** (stable foundation, never changes)
- **Extensions** (domain logic, can evolve)
- **Clean Separation** (no circular dependencies, no coupling)

### Why This Matters

Unlike traditional monolithic tools, Agency Toolkit is built for **long-term stability**:

✓ Core modules use **pure stdlib** (no external dependencies)
✓ Extensions can **evolve independently**
✓ **Zero circular dependencies** or tight coupling
✓ **Production-ready**, not "AI slop"

---

## Installation

```bash
# Clone repository
git clone <repository-url>
cd agency-toolkit

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Optional Dependencies

```bash
# For image generation (social posts)
pip install -e ".[imaging]"

# For PDF generation (briefings)
pip install -e ".[pdf]"

# For development/testing
pip install -e ".[dev]"
```

---

## Usage

### CLI Commands

Agency Toolkit provides a professional CLI interface:

```bash
# Show help
agency-toolkit --help

# Commands available:
#   social      - Generate social media posts
#   briefing    - Generate project briefings
#   structure   - Generate folder structures
#   batch       - Batch processing utilities
```

### Social Media Posts

**Generate single post:**
```bash
agency-toolkit social single "Hello World" \
  --style modern \
  --color "#000000" \
  --background "#FFFFFF" \
  --output ./output
```

**Batch generate from CSV:**
```bash
agency-toolkit social batch posts.csv --output ./output
```

CSV format:
```csv
text,style,color,background
"Launch announcement",modern,#000000,#FFFFFF
"Product update",minimal,#333333,#F5F5F5
```

### Project Briefings

**Generate single briefing:**
```bash
agency-toolkit briefing single \
  --client "Acme Corp" \
  --project "Website Redesign" \
  --type "Web Development" \
  --goals "Increase conversions,Improve UX" \
  --audience "B2B decision makers" \
  --timeline "3 months" \
  --budget "$50,000" \
  --deliverables "Wireframes,Designs,Development" \
  --output ./output \
  --format markdown
```

**Batch generate from CSV:**
```bash
agency-toolkit briefing batch briefings.csv --output ./output --format markdown
```

CSV format:
```csv
client_name,project_name,project_type,goals,target_audience,timeline,budget,deliverables,additional_notes
Acme Corp,Website Redesign,Web Development,Increase conversions|Improve UX,B2B decision makers,3 months,$50000,Wireframes|Designs|Development,Must be mobile-first
```

Note: Use `|` (pipe) to separate multiple goals or deliverables.

### Folder Structures

**List available templates:**
```bash
agency-toolkit structure list
```

Available templates:
- `agency_standard` - Standard agency project structure
- `social_media` - Social media campaign structure
- `web_project` - Web development project structure
- `branding` - Branding project structure

**Create folder structure:**
```bash
agency-toolkit structure create "My Project" \
  --type agency_standard \
  --path ./projects
```

**Create custom structure:**
```bash
agency-toolkit structure custom "My Project" \
  src tests docs assets \
  --path ./projects
```

---

## Architecture

### Frozen Core (8 Modules)

Located in `agency_core/` - **These never change:**

1. **asset_io.py** - File operations (read/write text, images, CSV, JSON, PDF)
2. **asset_storage.py** - In-memory key-value store with persistence
3. **template_schema.py** - Define and validate data structures
4. **asset_entity.py** - CRUD operations for assets
5. **content_transform.py** - Data transformations (e.g., markdown → PDF)
6. **workflow_process.py** - Multi-step workflow execution
7. **rule_validation.py** - Validation rules
8. **job_identity.py** - Job tracking and execution logs

**Design principles:**
- Pure stdlib only (no external dependencies)
- Simple, focused APIs
- Stateless where possible
- Testable

### Extensions

Located in `extensions/` - **These can evolve:**

1. **social_posts.py** - Social media post generation
2. **briefing_generator.py** - Project briefing generation
3. **folder_structure.py** - Folder structure templates
4. **batch_processor.py** - CSV batch processing

**Design principles:**
- Build on core modules only
- Can use external libraries
- Domain-specific logic
- Easy to add new extensions

---

## Python API

You can use Agency Toolkit programmatically:

```python
from extensions.social_posts import generate_social_post
from extensions.briefing_generator import generate_briefing, BriefingData
from extensions.folder_structure import generate_folder_structure

# Generate social post
post = generate_social_post(
    text="Hello World",
    style="modern",
    output_dir="./output"
)

# Generate briefing
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
briefing = generate_briefing(data, output_dir="./output")

# Generate folder structure
structure = generate_folder_structure(
    project_name="My Project",
    structure_type="agency_standard",
    base_path="./projects"
)
```

---

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=agency_core --cov=extensions
```

### Project Structure

```
agency-toolkit/
├── agency_core/          # Frozen core (8 modules)
│   ├── asset_io.py
│   ├── asset_storage.py
│   ├── template_schema.py
│   ├── asset_entity.py
│   ├── content_transform.py
│   ├── workflow_process.py
│   ├── rule_validation.py
│   └── job_identity.py
├── extensions/           # Domain extensions
│   ├── social_posts.py
│   ├── briefing_generator.py
│   ├── folder_structure.py
│   └── batch_processor.py
├── tests/               # Test suite
├── examples/            # Usage examples
├── cli.py              # CLI interface
├── setup.py            # Package setup
└── README.md           # This file
```

---

## Why Genesis Core?

Traditional agency tools suffer from:
- **Circular dependencies** (module A needs B, B needs A)
- **Tight coupling** (changing one thing breaks everything)
- **AI slop** (unstable, unreliable generated code)

Genesis Core solves this:

1. **Stable Foundation**: Core modules are simple, tested, and frozen
2. **Clean Architecture**: Extensions build on core, never the reverse
3. **Easy Maintenance**: Change extensions without touching core
4. **Production-Ready**: Built for real agency work, not demos

---

## Examples

See the `examples/` directory for:
- CSV templates for batch processing
- Sample workflows
- Integration examples

---

## License

MIT License - See LICENSE file for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes (preferably to extensions, not core)
4. Add tests
5. Submit a pull request

**Note**: Changes to `agency_core/` modules require strong justification and should be rare.

---

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

# 🌌 TalentMatchAI

TalentMatchAI (codename **TamatAI**) is a Streamlit application that helps recruiters
compare job descriptions with candidate CVs. It converts uploaded PDFs into images,
feeds them to a Groq-backed LangChain agent, and returns ranked matches enriched with
summaries and metadata.

## ✨ Key features
- **Job & CV ingestion** – upload one job post and multiple CVs in PDF format.
- **Automated scoring** – Groq + Langfuse powered agent extracts insights and
  produces structured ranking data.
- **Rich UI** – modern Streamlit interface with previews, metrics, and tables.
- **Batch processing** – handle multiple candidates in a single run.

## 📦 Requirements
- Python 3.11+
- Poppler utilities (`poppler-utils`) – required by `pdf2image`
- GROQ and Langfuse credentials (see environment variables below)

## 🔐 Environment variables
| Variable | Description | Default |
| --- | --- | --- |
| `GROQ_API_KEY` | API key for Groq's LLM endpoint | `""` |
| `LANGFUSE_SECRET_KEY` | Secret key for Langfuse tracing | `""` |
| `LANGFUSE_PUBLIC_KEY` | Public key for Langfuse tracing | `""` |
| `LANGFUSE_HOST` | Langfuse API host | `"https://cloud.langfuse.com"` |
| `LANGFUSE_SYSTEM_PROMPT_NAME` | Langfuse prompt to load (use `match`) | `"match"` |

Obtain the Groq key directly from [console.groq.com](https://console.groq.com) and
create Langfuse credentials plus a prompt named `match` in
[cloud.langfuse.com](https://cloud.langfuse.com). Set
`LANGFUSE_SYSTEM_PROMPT_NAME="match"` so the app loads that prompt configuration
during startup.

Store sensitive values in a `.env` file or pass them when launching Docker containers.

## 🚀 Local development
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
streamlit run tamatai/app.py
```

### Running tests
Pytest is configured in CI, but you can run it locally as well:
```bash
pytest --cov=tamatai
```

## 🐳 Running with Docker
Build the image locally:
```bash
docker build -t talentmatchai .
```

Run the container (exposes Streamlit on port 8501 by default):
```bash
docker run --rm -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  -e LANGFUSE_SECRET_KEY=your_langfuse_secret \
  -e LANGFUSE_PUBLIC_KEY=your_langfuse_public \
  -e LANGFUSE_SYSTEM_PROMPT_NAME=match \
  talentmatchai
```

after which the UI is available at `http://localhost:8501`.

## 📂 Project structure
```
├── Dockerfile
├── pyproject.toml
├── README.md
├── tamatai/
│   ├── app.py          # Streamlit interface
│   ├── chain/
│   │   ├── helper.py   # Prompt utilities and pdf helpers
│   │   └── match.py    # Matching engine
│   ├── config.py       # Pydantic settings
│   └── logging.py
└── tests/              # Pytest suite
```

## 🧪 Continuous integration
GitHub Actions workflow `test-ci.yml` installs dependencies, executes pytest with
coverage, and publishes a summary. Any new functionality should include unit tests
so the workflow remains green.

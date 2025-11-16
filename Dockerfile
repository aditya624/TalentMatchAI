FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=on \
    PORT=8501

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    poppler-utils \
 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY tamatai ./tamatai

RUN python -m pip install --upgrade pip \
 && pip install .

# Copy the remaining source (tests, workflows, etc.) for completeness
COPY . .

EXPOSE 8501

ENTRYPOINT ["/bin/sh", "-c", "streamlit run tamatai/app.py --server.address=0.0.0.0 --server.port=${PORT:-8501}"]

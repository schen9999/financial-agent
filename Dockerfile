# FastAPI backend image for ECS Fargate.
# Large by nature: the API import chain (cache.py / rag.py) loads a HuggingFace
# embedding model, pulling in torch + transformers + sentence-transformers +
# llama-index + langchain. We bake the model into the image so it doesn't
# download on cold start.
FROM python:3.13-slim

# libgomp1: OpenMP runtime needed by torch / scikit-learn wheels.
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/hf-cache \
    HF_HUB_DISABLE_TELEMETRY=1 \
    TOKENIZERS_PARALLELISM=false \
    TRANSFORMERS_VERBOSITY=error

WORKDIR /app

# Dependencies first for layer caching.
COPY requirements-api.txt .
RUN pip install -r requirements-api.txt

# Bake the bge-small embedding model into the image (same load path cache.py /
# rag.py use at runtime), so container start doesn't hit the HF Hub.
RUN mkdir -p /opt/hf-cache && \
    python -c "from llama_index.embeddings.huggingface import HuggingFaceEmbedding; HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')"

# Application code (.dockerignore keeps out .env, notebooks, data, tests, etc.).
COPY . .

EXPOSE 8000

# Generous start period: model load + table init on first boot is slow.
HEALTHCHECK --interval=30s --timeout=5s --start-period=180s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health', timeout=3).status==200 else 1)"

# Single worker: the model is loaded per process; one copy fits the 3 GB task.
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

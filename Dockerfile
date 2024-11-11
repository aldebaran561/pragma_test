# ---- Base python ----
FROM python:3.12 AS base
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
COPY requirements.txt requirements.txt
RUN python -m venv /venv \
    && . /venv/bin/activate \
    && pip install --upgrade pip \
    && pip install --requirement requirements.txt

# ---- Builder ----
FROM dependencies AS builder
COPY . .

# --- Release with Slim ----
FROM python:3.12-slim AS runner
WORKDIR /app
RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

COPY --from=dependencies /venv /venv
COPY --from=dependencies /root/.cache /root/.cache

# --- Install dependencies ----
COPY --from=builder /app /app

# --- Set environment variables for virtualenv ---
ENV PATH="/venv/bin:$PATH"

RUN addgroup --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8001

# --- Run the app ---
CMD ["python", "-m", "app.main"]

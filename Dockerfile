# ---------- Stage 1: build ----------
FROM python:3.12-slim AS build
WORKDIR /w
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.12-slim
RUN useradd -r -u 10001 appuser
WORKDIR /app
COPY --from=build /install /usr/local
COPY app/ .
ENV APP_VERSION=v1
USER appuser
EXPOSE 8080
# image slim không có curl → dùng chính Python để gọi /health
HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

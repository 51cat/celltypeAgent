FROM python:3.10-slim

WORKDIR /app

COPY setup.py .
COPY ohmycelltype/ ./ohmycelltype/
COPY README.md .

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["ohmycelltype"]
CMD ["--help"]

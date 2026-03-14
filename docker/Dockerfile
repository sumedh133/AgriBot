FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .

CMD ["uv", "run", "streamlit", "run", "app/main.py", "--server.port=$PORT", "--server.headless=true"]
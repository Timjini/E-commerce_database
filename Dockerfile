FROM python:3.9-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .

FROM base as debugger
RUN pip install debugpy
ENTRYPOINT [ "python","-m","debugpy","--listen","0.0.0.0:5678","--wait-for-client","-m" ]

FROM base as primay

CMD ["/app/entrypoint.sh"]

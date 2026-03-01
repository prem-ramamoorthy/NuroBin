ARG PG_MAJOR=16
FROM postgres:${PG_MAJOR}-bookworm

RUN apt-get update && apt-get install -y \
  postgresql-${PG_MAJOR}-postgis-3 \
  postgresql-${PG_MAJOR}-postgis-3-scripts \
  postgresql-${PG_MAJOR}-pgvector \
  && rm -rf /var/lib/apt/lists/*

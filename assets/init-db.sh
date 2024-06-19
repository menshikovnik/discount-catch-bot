#!/bin/bash
set -e  # Выходить из скрипта при любой ошибке

# Название базы данных
DATABASE_NAME=bot_db

# Подключаемся к PostgreSQL и создаем базу данных
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE $DATABASE_NAME;
EOSQL

# Восстанавливаем данные из дампа
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="$DATABASE_NAME" < /docker-entrypoint-initdb.d/dump.sql

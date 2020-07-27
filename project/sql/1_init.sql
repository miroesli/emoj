\connect postgres
DROP DATABASE IF EXISTS project;
CREATE DATABASE project;
-- DROP USER IF EXISTS toggleme;
-- CREATE USER toggleme WITH PASSWORD 'ss' CREATEDB;
-- ALTER USER toggleme CREATEDB;
ALTER ROLE toggleme SET client_encoding TO 'utf8';
ALTER ROLE toggleme SET default_transaction_isolation TO 'read committed';
ALTER ROLE toggleme SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE project TO toggleme;
\connect project
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

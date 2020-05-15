CREATE DATABASE project;
CREATE USER toggleme WITH PASSWORD 'ss';
ALTER ROLE toggleme SET client_encoding TO 'utf8';
ALTER ROLE toggleme SET default_transaction_isolation TO 'read committed';
ALTER ROLE toggleme SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE project TO toggleme;

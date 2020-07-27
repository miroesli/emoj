FROM postgres:alpine

# COPY *.sql /docker-entrypoint-initdb.d/
# COPY ./docker/db/init.sh /docker-entrypoint-initdb.d/
# Copy init.sh /docker-entrypoint-initdb.d/

ADD sql/1_init.sql /docker-entrypoint-initdb.d
ADD sql/2_create.sql /docker-entrypoint-initdb.d
ADD sql/3_test_data.sql /docker-entrypoint-initdb.d
RUN chmod a+r /docker-entrypoint-initdb.d/*
# CMD ls -la /docker-entrypoint-initdb.d

# CMD ls -la /etc
# WORKDIR ./docker-entrypoint-initdb.d
# CMD ["sh", "init.sh"]
# EXPOSE 5432

FROM @dockerRegistry/@ImageSqlMigrationExecutor
COPY migration migrations/
USER root
RUN chown -R inspire:inspire /home/inspire/migrations/*
USER inspire

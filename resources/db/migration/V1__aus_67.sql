DROP TABLE IF EXISTS TEST_CONFIG;

CREATE TABLE TEST_CONFIG
(
    BRAND               VARCHAR(50)  NOT NULL,
    TYPE                VARCHAR(50)  NOT NULL,
    CONFIG_KEY          VARCHAR(50)  NOT NULL,
    VALUE               VARCHAR(50)  NOT NULL,
    CREATED_TS          DATETIME2(7) NOT NULL,
    UPDATED_TS          DATETIME2(7) NOT NULL,
    UPDATED_USER_ID     VARCHAR(50)
    CONSTRAINT PK_application_config PRIMARY KEY (BRAND, TYPE, CONFIG_KEY)
);
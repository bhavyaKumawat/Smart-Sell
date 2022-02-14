
DROP TABLE IF EXISTS TEST_EVENTS;

CREATE TABLE TEST_EVENTS
(
    id                  VARCHAR(255) NOT NULL,
    brand               VARCHAR(5) NOT NULL,
    first_name          VARCHAR(255) NOT NULL,
    last_name           VARCHAR(255) NOT NULL,
    customer_id         VARCHAR(255) NOT NULL,
    emails              VARCHAR(255) NOT NULL,

    created_ts          DATETIMEOFFSET(7) NOT NULL,
    CONSTRAINT PK_OfferEvents PRIMARY KEY (id)
);

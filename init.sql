CREATE TABLE IF NOT EXISTS support_tickets (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    issue TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'in_progress', 'resolved'))
);

INSERT INTO support_tickets (customer_name, issue, status)
VALUES
    ('Ada Okafor', 'API returns HTTP 500', 'open'),
    ('Chidi Eze', 'Database connection timeout', 'in_progress'),
    ('Grace Nwosu', 'Ticket endpoint returns no data', 'resolved')
;

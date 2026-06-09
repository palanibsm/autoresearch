-- Banking Database Schema
-- Intentionally designed with optimization opportunities

CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    country_code VARCHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    account_type VARCHAR(50),
    balance DECIMAL(15,2),
    currency VARCHAR(3),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    from_account_id INTEGER REFERENCES accounts(account_id),
    to_account_id INTEGER REFERENCES accounts(account_id),
    amount DECIMAL(15,2),
    currency VARCHAR(3),
    transaction_type VARCHAR(50),
    status VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    principal_amount DECIMAL(15,2),
    interest_rate DECIMAL(5,2),
    term_months INTEGER,
    status VARCHAR(20),
    disbursement_date DATE,
    maturity_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loan_payments (
    payment_id BIGSERIAL PRIMARY KEY,
    loan_id INTEGER REFERENCES loans(loan_id),
    amount DECIMAL(15,2),
    payment_date DATE,
    principal_paid DECIMAL(15,2),
    interest_paid DECIMAL(15,2),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    transaction_id BIGINT REFERENCES transactions(transaction_id),
    customer_id INTEGER REFERENCES customers(customer_id),
    alert_type VARCHAR(100),
    risk_score DECIMAL(5,2),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    notes TEXT
);

-- Populate with synthetic banking data
INSERT INTO customers (name, email, phone, country_code) VALUES
('Raj Kumar', 'raj.kumar@example.com', '+6581234567', 'SG'),
('Priya Sharma', 'priya.sharma@example.com', '+6587654321', 'SG'),
('Chen Wei', 'chen.wei@example.com', '+6589876543', 'SG'),
('Mohammed Ali', 'moh.ali@example.com', '+6582468135', 'MY'),
('Lisa Wong', 'lisa.wong@example.com', '+6591357924', 'SG'),
('Arun Pillai', 'arun.pillai@example.com', '+6583579246', 'SG'),
('Fatimah Hassan', 'fatimah.hassan@example.com', '+6584682468', 'SG'),
('David Tan', 'david.tan@example.com', '+6585791113', 'SG'),
('Siti Nurhaliza', 'siti.nur@example.com', '+6586801224', 'MY'),
('Vikram Singh', 'vikram.singh@example.com', '+6587912335', 'SG');

INSERT INTO customers (name, email, phone, country_code) VALUES
('Amy Lee', 'amy.lee@example.com', '+6588023446', 'SG'),
('Badriyah Khalil', 'badriyah.k@example.com', '+6589134557', 'SG'),
('Chew Hong', 'chew.hong@example.com', '+6580245668', 'SG'),
('Dinesh Kumar', 'dinesh.k@example.com', '+6581356779', 'SG'),
('Esther Lim', 'esther.lim@example.com', '+6582467880', 'SG'),
('Farrah Khan', 'farrah.khan@example.com', '+6583578991', 'MY'),
('Ganesan Murthy', 'ganesan.m@example.com', '+6584689002', 'SG'),
('Hannah Ng', 'hannah.ng@example.com', '+6585790113', 'SG'),
('Ibrahim Hassan', 'ibrahim.h@example.com', '+6586801224', 'SG'),
('Jessica Teo', 'jessica.teo@example.com', '+6587912335', 'SG');

INSERT INTO accounts (customer_id, account_type, balance, currency, status) VALUES
(1, 'SAVINGS', 50000.00, 'SGD', 'ACTIVE'),
(1, 'CHECKING', 25000.00, 'SGD', 'ACTIVE'),
(2, 'SAVINGS', 75000.00, 'SGD', 'ACTIVE'),
(2, 'CHECKING', 15000.00, 'SGD', 'ACTIVE'),
(3, 'SAVINGS', 120000.00, 'SGD', 'ACTIVE'),
(3, 'CHECKING', 30000.00, 'SGD', 'ACTIVE'),
(4, 'SAVINGS', 45000.00, 'MYR', 'ACTIVE'),
(5, 'SAVINGS', 80000.00, 'SGD', 'ACTIVE'),
(6, 'CHECKING', 20000.00, 'SGD', 'ACTIVE'),
(7, 'SAVINGS', 95000.00, 'SGD', 'ACTIVE'),
(8, 'CHECKING', 35000.00, 'SGD', 'ACTIVE'),
(9, 'SAVINGS', 60000.00, 'MYR', 'ACTIVE'),
(10, 'CHECKING', 18000.00, 'SGD', 'ACTIVE'),
(11, 'SAVINGS', 110000.00, 'SGD', 'ACTIVE'),
(12, 'CHECKING', 22000.00, 'SGD', 'ACTIVE');

-- Generate transactions (bulk insert for realistic load)
INSERT INTO transactions (from_account_id, to_account_id, amount, currency, transaction_type, status, description)
SELECT
    (floor(random() * 15)::int) + 1 as from_account,
    (floor(random() * 15)::int) + 1 as to_account,
    (random() * 10000 + 100)::DECIMAL as amount,
    CASE WHEN random() > 0.3 THEN 'SGD' ELSE 'MYR' END as currency,
    CASE WHEN random() > 0.5 THEN 'TRANSFER' ELSE 'PAYMENT' END as type,
    'COMPLETED' as status,
    'Bulk transaction ' || generate_series(1, 500) as description
FROM generate_series(1, 500);

-- Generate loans
INSERT INTO loans (customer_id, principal_amount, interest_rate, term_months, status, disbursement_date, maturity_date)
SELECT
    ((generate_series(1, 50) - 1) % 10) + 1 as customer_id,
    (random() * 500000 + 50000)::DECIMAL as principal,
    (random() * 5 + 2)::DECIMAL as interest_rate,
    (floor(random() * 300) + 12)::INTEGER as term,
    CASE WHEN random() > 0.2 THEN 'ACTIVE' ELSE 'CLOSED' END as status,
    CURRENT_DATE - INTERVAL '1 day' * (floor(random() * 730))::INTEGER as disburse_date,
    CURRENT_DATE + INTERVAL '1 day' * (floor(random() * 730))::INTEGER as mature_date
FROM (SELECT generate_series(1, 50)) as t(customer_id);

-- Generate loan payments
INSERT INTO loan_payments (loan_id, amount, payment_date, principal_paid, interest_paid, status)
SELECT
    ((generate_series(1, 200) - 1) % 50) + 1 as loan_id,
    (random() * 5000 + 1000)::DECIMAL as amount,
    CURRENT_DATE - INTERVAL '1 day' * (floor(random() * 365))::INTEGER as payment_date,
    (random() * 4000 + 500)::DECIMAL as principal,
    (random() * 1500 + 100)::DECIMAL as interest,
    CASE WHEN random() > 0.1 THEN 'COMPLETED' ELSE 'PENDING' END as status
FROM (SELECT generate_series(1, 200)) as t(loan_id);

-- Generate fraud alerts
INSERT INTO fraud_alerts (transaction_id, customer_id, alert_type, risk_score, status, notes)
SELECT
    (transaction_id % 500) + 1 as transaction_id,
    (customer_id % 20) + 1 as customer_id,
    CASE
        WHEN random() > 0.7 THEN 'UNUSUAL_AMOUNT'
        WHEN random() > 0.4 THEN 'VELOCITY_CHECK'
        ELSE 'LOCATION_MISMATCH'
    END as alert_type,
    (random() * 100)::DECIMAL as risk_score,
    CASE WHEN random() > 0.5 THEN 'RESOLVED' ELSE 'PENDING' END as status,
    'Fraud detection alert ' || generate_series(1, 100) as notes
FROM generate_series(1, 100) as transaction_id;

-- Create some intentionally slow/problematic indexes to demonstrate optimization
-- These will be the "before" state that the optimizer will improve

COMMIT;

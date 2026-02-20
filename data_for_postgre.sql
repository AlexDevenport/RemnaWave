TRUNCATE TABLE operations, clients RESTART IDENTITY CASCADE;

INSERT INTO clients (id, status, expires_at, created_at, updated_at) VALUES
(gen_random_uuid(), 'active',   NOW() + INTERVAL '30 days', NOW(), NOW()),
(gen_random_uuid(), 'blocked',  NOW() + INTERVAL '30 days', NOW(), NOW()),
(gen_random_uuid(), 'active',   NOW() - INTERVAL '5 days',  NOW(), NOW()),
(gen_random_uuid(), 'active',   NOW() + INTERVAL '7 days',  NOW(), NOW());

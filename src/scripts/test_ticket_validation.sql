-- Script SQL para teste de validação de ingressos

-- =====================================================
-- CRIAÇÃO DE USUÁRIOS
-- =====================================================

-- Senha: 123
INSERT INTO users (name, email, hashed_password, role) 
VALUES ('Staff Teste', 'staff@test.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'STAFF');

-- Senha: 123
INSERT INTO users (name, email, hashed_password, role) 
VALUES ('Organizador Teste', 'organizer@test.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'ORGANIZER');

INSERT INTO users (name, email, hashed_password, role) 
VALUES ('Staff 2', 'staff2@test.com', '', 'STAFF');

INSERT INTO users (name, email, hashed_password, role) 
VALUES ('Staff 3', 'staff3@test.com', '', 'STAFF');

INSERT INTO users (name, email, hashed_password, role) 
VALUES ('Cliente Teste', 'cliente@test.com', '', 'CLIENT');

INSERT INTO users (name, email, hashed_password, role) 
VALUES ('Organizador 2', 'organizer2@test.com', '', 'ORGANIZER');

-- =====================================================
-- CENÁRIOS PARA STAFF (1-4)
-- =====================================================

-- Cenário 1: Evento não existente
INSERT INTO tickets (event_id, client_id, code, status, created_at) 
VALUES (
    9999,
    5,
    'TKT001',
    'PENDING',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
);

-- Cenário 2: Evento fora do período de validação
INSERT INTO events (created_at, end_date, location, name, start_date, tickets_available, organizer_id, staffs_id)
VALUES (
    '2024-01-01T10:00:00Z',
    '2024-01-05T22:00:00Z',
    'Local Teste A',
    'Evento Expirado',
    '2024-01-05T18:00:00Z',
    100,
    2,
    '1,3,4'
);

INSERT INTO tickets (event_id, client_id, code, status, created_at) 
VALUES (
    1,
    5,
    'TKT002',
    'PENDING',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
);

-- Cenário 3: Evento válido - STAFF autorizado
INSERT INTO events (created_at, end_date, location, name, start_date, tickets_available, organizer_id, staffs_id)
VALUES (
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    '2026-12-31T23:59:59Z',
    'Local Teste B',
    'Evento Válido com Staff',
    '2025-10-01T00:00:00Z',
    200,
    2,
    '1,3,4'
);

INSERT INTO tickets (event_id, client_id, code, status, created_at) 
VALUES (
    2,
    5,
    'TKT003',
    'PENDING',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
);

-- Cenário 4: Evento válido - STAFF NÃO autorizado
INSERT INTO events (created_at, end_date, location, name, start_date, tickets_available, organizer_id, staffs_id)
VALUES (
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    '2026-12-31T23:59:59Z',
    'Local Teste C',
    'Evento Válido sem Staff',
    '2025-10-01T00:00:00Z',
    150,
    2,
    '3,4'
);

INSERT INTO tickets (event_id, client_id, code, status, created_at) 
VALUES (
    3,
    5,
    'TKT004',
    'PENDING',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
);

-- =====================================================
-- CENÁRIOS PARA ORGANIZER (5-7)
-- =====================================================

-- Cenário 5: Evento válido - ORGANIZER é o dono
INSERT INTO events (created_at, end_date, location, name, start_date, tickets_available, organizer_id, staffs_id)
VALUES (
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    '2026-12-31T23:59:59Z',
    'Local Teste D',
    'Evento do Organizador',
    '2025-10-01T00:00:00Z',
    180,
    2,
    ''
);

INSERT INTO tickets (event_id, client_id, code, status, created_at) 
VALUES (
    4,
    5,
    'TKT005',
    'PENDING',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
);

-- Cenário 6: Evento válido - ORGANIZER NÃO é o dono
INSERT INTO events (created_at, end_date, location, name, start_date, tickets_available, organizer_id, staffs_id)
VALUES (
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    '2026-12-31T23:59:59Z',
    'Local Teste E',
    'Evento de Outro Organizador',
    '2025-10-01T00:00:00Z',
    220,
    6,
    ''
);

INSERT INTO tickets (event_id, client_id, code, status, created_at) 
VALUES (
    5,
    5,
    'TKT006',
    'PENDING',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
);

-- Cenário 7: Evento válido - Ingresso JÁ validado
INSERT INTO events (created_at, end_date, location, name, start_date, tickets_available, organizer_id, staffs_id)
VALUES (
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    '2026-12-31T23:59:59Z',
    'Local Teste F',
    'Evento do Organizador 2',
    '2025-10-01T00:00:00Z',
    300,
    2,
    ''
);

INSERT INTO tickets (event_id, client_id, code, status, created_at) 
VALUES (
    6,
    5,
    'TKT007',
    'VALIDATED',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
);

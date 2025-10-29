# Guia de Teste - Validação de Ingressos

## Como Executar os Testes

1. **Preparar o banco de dados:**

   **1.1 Remover o banco de dados existente:**

   ```bash
   rm data/app.db
   ```

   **1.2 Executar o aplicativo para recriar o banco de dados:**

   ```bash
   make run
   ```

   **1.3 Executar o script de teste:**

   ```bash
   sqlite3 data/app.db < src/scripts/test_ticket_validation.sql
   ```

## Query de Visualização

Para visualizar todos os tickets com suas informações de evento relevantes:

```sql
SELECT
    t.code AS ticket_code,
    t.status AS ticket_status,
    t.client_id,
    e.id AS event_id,
    e.name AS event_name,
    e.start_date,
    e.end_date,
    e.organizer_id,
    e.staffs_id
FROM tickets t
LEFT JOIN events e ON t.event_id = e.id
ORDER BY t.code;
```

## Cenários para STAFF (1-4)

**Login:** Staff (staff@test.com / 123)

### Cenário 1: Evento Não Existente

**Código do Ingresso:** `TKT001`

**Resultado Esperado:**

- ❌ Erro: `Event with ID '9999' not found for ticket validation.`

---

### Cenário 2: Evento Fora do Período

**Código do Ingresso:** `TKT002`

**Resultado Esperado:**

- ❌ Erro: `Ticket validation is only allowed between 2024-01-05 18:00:00+00:00 and 2024-01-05 22:00:00+00:00 for event ID 1.`

**Motivo:** O evento já terminou em janeiro de 2024.

---

### Cenário 3: Validação Bem-Sucedida

**Código do Ingresso:** `TKT003`

**Resultado Esperado:**

- ✅ Ingresso validado com sucesso
- Status alterado de `PENDING` para `VALIDATED`

**Motivo:** Staff está autorizado e evento está no período válido.

---

### Cenário 4: Staff Não Autorizado

**Código do Ingresso:** `TKT004`

**Resultado Esperado:**

- ❌ Erro: `User with ID '1' and role 'STAFF' is not authorized to validate ticket with code: TKT004.`

**Motivo:** O Staff Teste não está na lista de staffs autorizados deste evento.

---

## Cenários para ORGANIZER (5-7)

**Login:** Organizer (organizer@test.com / 123)

### Cenário 5: Validação Bem-Sucedida

**Código do Ingresso:** `TKT005`

**Resultado Esperado:**

- ✅ Ingresso validado com sucesso
- Status alterado de `PENDING` para `VALIDATED`

**Motivo:** Organizador é o dono do evento.

---

### Cenário 6: Organizador Não Autorizado

**Código do Ingresso:** `TKT006`

**Resultado Esperado:**

- ❌ Erro: `User with ID '2' and role 'ORGANIZER' is not authorized to validate ticket with code: TKT006.`

**Motivo:** Este evento pertence a outro organizador (ID 6).

---

### Cenário 7: Ingresso Já Validado

**Código do Ingresso:** `TKT007`

**Resultado Esperado:**

- ❌ Erro: `Ticket has already been validated.`

**Motivo:** Este ingresso já possui status `VALIDATED`.

---

## Resumo dos Resultados

| Cenário | Ator      | Código | Resultado            | Motivo                      |
| ------- | --------- | ------ | -------------------- | --------------------------- |
| 1       | STAFF     | TKT001 | ❌ Evento não existe | Evento ID 9999 não existe   |
| 2       | STAFF     | TKT002 | ❌ Fora do período   | Evento expirado             |
| 3       | STAFF     | TKT003 | ✅ Sucesso           | Staff autorizado            |
| 4       | STAFF     | TKT004 | ❌ Não autorizado    | Staff não está na lista     |
| 5       | ORGANIZER | TKT005 | ✅ Sucesso           | Organizador é o dono        |
| 6       | ORGANIZER | TKT006 | ❌ Não autorizado    | Evento de outro organizador |
| 7       | ORGANIZER | TKT007 | ❌ Já validado       | Status VALIDATED            |

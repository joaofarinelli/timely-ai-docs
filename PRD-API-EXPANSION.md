# PRD — Expansão da API Pública Timely.ai v1

**Versão:** 1.0
**Data:** 2026-03-02
**Autor:** Time de Engenharia Timely.ai

---

## 1. Visão Geral

### 1.1 Objetivo
Expandir a API pública do Timely.ai para cobrir todas as funcionalidades da plataforma, replicando e adaptando o escopo completo de endpoints disponíveis na API do GPT Maker (referência: `developer.gptmaker.ai`), adaptados ao domínio e arquitetura do Timely.ai.

### 1.2 Estado Atual (AS-IS)
A API pública atual (`api.timelyai.com.br/v1`) possui **21 operações** em **6 grupos**:

| Grupo | Endpoints | Operações |
|-------|-----------|-----------|
| System | `/v1/health`, `/v1/me` | 2 GET |
| Contacts | `/v1/contacts`, `/v1/contacts/{id}` | 5 (CRUD + list) |
| Leads | `/v1/leads`, `/v1/leads/{id}` | 5 (CRUD + list) |
| Opportunities | `/v1/opportunities`, `/v1/opportunities/{id}` | 5 (CRUD + list) |
| Pipeline | `/v1/pipeline/columns` | 1 GET |
| Conversations | `/v1/conversations`, `/v1/conversations/{id}`, `/v1/conversations/{id}/messages` | 3 GET |

### 1.3 Estado Desejado (TO-BE)
Expandir para **~80+ operações** em **14 grupos**, adicionando 8 novos domínios:

| Novo Grupo | Descrição | Operações Estimadas |
|------------|-----------|---------------------|
| **Agents** | CRUD de agentes, configurações, ativação/desativação, webhooks, histórico | ~16 |
| **Channels** | Canais de comunicação (WhatsApp, Telegram, Widget, etc.) | ~11 |
| **Chats** | Mensagens, atendimento humano, envio de mensagens | ~9 |
| **Custom Fields** | Campos personalizados do workspace | ~4 |
| **Intentions** | Intenções/ações de API dos agentes | ~4 |
| **Idle Actions** | Ações por inatividade | ~4 |
| **Transfer Rules** | Regras de transferência entre agentes | ~4 |
| **MCP** | Conexões Model Context Protocol | ~7 |
| **Interactions** | Sessões de atendimento (analytics) | ~3 |
| **Workspace** | Gestão de workspaces e créditos | ~3 |
| **Trainings** (ext.) | Gerenciamento de treinamentos (extra ao agente) | ~2 |

**Além disso**, expandir endpoints existentes:
- **Conversations**: adicionar `POST` para envio de mensagens, `DELETE` para chat, `PUT` para handoff humano
- **Contacts**: adicionar busca avançada por workspace

### 1.4 Métricas de Sucesso
- 100% dos endpoints do GPT Maker replicados e adaptados ao Timely.ai
- Documentação OpenAPI 3.1.0 completa para cada endpoint
- Documentação Mintlify atualizada com novos grupos no sidebar
- Zero breaking changes nos endpoints existentes
- Cobertura de testes na documentação (exemplos de request/response)

---

## 2. Requisitos Funcionais

### 2.1 Autenticação & Autorização
- Manter `x-api-key` via header
- Adicionar novos scopes:
  - `agents:read`, `agents:write`
  - `channels:read`, `channels:write`
  - `chats:read`, `chats:write`
  - `custom-fields:read`, `custom-fields:write`
  - `intentions:read`, `intentions:write`
  - `idle-actions:read`, `idle-actions:write`
  - `transfer-rules:read`, `transfer-rules:write`
  - `mcp:read`, `mcp:write`
  - `interactions:read`
  - `workspaces:read`
  - `trainings:read`, `trainings:write`
- Atualizar `GET /v1/me` para retornar novos scopes

### 2.2 Padrões de API (manter consistência)
- Versionamento: `/v1/`
- Paginação: `page`, `limit`, `sort`, `order`, `search`
- Respostas: `{ "data": ... }` ou `{ "data": [...], "pagination": {...} }`
- Erros: `{ "error": { "code": "...", "message": "...", "status": N } }`
- Rate limiting: 100 req/min por API key (headers `X-RateLimit-*`)

---

## 3. Especificação dos Endpoints

### 3.1 AGENTS — Gerenciamento de Agentes IA

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `POST` | `/v1/agents` | Criar agente | `agents:write` |
| `GET` | `/v1/agents` | Listar agentes | `agents:read` |
| `GET` | `/v1/agents/{id}` | Obter agente | `agents:read` |
| `PUT` | `/v1/agents/{id}` | Atualizar agente | `agents:write` |
| `DELETE` | `/v1/agents/{id}` | Deletar agente | `agents:write` |
| `POST` | `/v1/agents/{id}/activate` | Ativar agente | `agents:write` |
| `POST` | `/v1/agents/{id}/deactivate` | Desativar agente | `agents:write` |
| `GET` | `/v1/agents/{id}/settings` | Obter configurações | `agents:read` |
| `PUT` | `/v1/agents/{id}/settings` | Atualizar configurações | `agents:write` |
| `GET` | `/v1/agents/{id}/webhooks` | Obter webhooks | `agents:read` |
| `PUT` | `/v1/agents/{id}/webhooks` | Atualizar webhooks | `agents:write` |
| `POST` | `/v1/agents/{id}/conversation` | Conversar com agente | `agents:write` |
| `POST` | `/v1/agents/{id}/context` | Adicionar contexto | `agents:write` |
| `GET` | `/v1/agents/{id}/credits` | Consumo de créditos | `agents:read` |
| `GET` | `/v1/agents/{id}/behavior-history` | Histórico de comportamento | `agents:read` |

### 3.2 TRAININGS — Treinamentos de Agentes

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `POST` | `/v1/agents/{id}/trainings` | Criar treinamento | `trainings:write` |
| `GET` | `/v1/agents/{id}/trainings` | Listar treinamentos | `trainings:read` |
| `PUT` | `/v1/trainings/{id}` | Atualizar treinamento | `trainings:write` |
| `DELETE` | `/v1/trainings/{id}` | Deletar treinamento | `trainings:write` |

### 3.3 CHANNELS — Canais de Comunicação

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `POST` | `/v1/channels` | Criar canal | `channels:write` |
| `GET` | `/v1/channels` | Listar canais | `channels:read` |
| `PUT` | `/v1/channels/{id}` | Editar canal | `channels:write` |
| `DELETE` | `/v1/channels/{id}` | Remover canal | `channels:write` |
| `GET` | `/v1/channels/{id}/config` | Obter configuração | `channels:read` |
| `PUT` | `/v1/channels/{id}/config` | Atualizar configuração | `channels:write` |
| `GET` | `/v1/channels/{id}/qr-code` | Obter QR code | `channels:read` |
| `POST` | `/v1/channels/{id}/conversation` | Iniciar conversa | `channels:write` |
| `GET` | `/v1/channels/{id}/widget/links` | Obter links do widget | `channels:read` |
| `PUT` | `/v1/channels/{id}/widget/settings` | Atualizar config do widget | `channels:write` |

### 3.4 CHATS — Mensagens e Atendimento (expandir Conversations)

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `GET` | `/v1/conversations` | Listar conversas | `conversations:read` *(existe)* |
| `GET` | `/v1/conversations/{id}` | Obter conversa | `conversations:read` *(existe)* |
| `GET` | `/v1/conversations/{id}/messages` | Listar mensagens | `messages:read` *(existe)* |
| `POST` | `/v1/conversations/{id}/messages` | **Enviar mensagem** | `chats:write` *(NOVO)* |
| `PUT` | `/v1/conversations/{id}/messages/{messageId}` | **Editar mensagem** | `chats:write` *(NOVO)* |
| `DELETE` | `/v1/conversations/{id}/messages/{messageId}` | **Deletar mensagem** | `chats:write` *(NOVO)* |
| `DELETE` | `/v1/conversations/{id}/messages` | **Limpar mensagens** | `chats:write` *(NOVO)* |
| `DELETE` | `/v1/conversations/{id}` | **Deletar conversa** | `chats:write` *(NOVO)* |
| `POST` | `/v1/conversations/{id}/human-handoff` | **Iniciar atendimento humano** | `chats:write` *(NOVO)* |
| `POST` | `/v1/conversations/{id}/ai-resume` | **Retomar atendimento IA** | `chats:write` *(NOVO)* |

### 3.5 CUSTOM FIELDS — Campos Personalizados

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `POST` | `/v1/custom-fields` | Criar campo | `custom-fields:write` |
| `GET` | `/v1/custom-fields` | Listar campos | `custom-fields:read` |
| `PUT` | `/v1/custom-fields/{id}` | Atualizar campo | `custom-fields:write` |
| `PUT` | `/v1/custom-fields/{id}/archive` | Arquivar/desarquivar campo | `custom-fields:write` |

### 3.6 INTENTIONS — Intenções (Ações de API)

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `POST` | `/v1/agents/{id}/intentions` | Criar intenção | `intentions:write` |
| `GET` | `/v1/agents/{id}/intentions` | Listar intenções | `intentions:read` |
| `PUT` | `/v1/intentions/{id}` | Atualizar intenção | `intentions:write` |
| `DELETE` | `/v1/intentions/{id}` | Deletar intenção | `intentions:write` |

### 3.7 IDLE ACTIONS — Ações por Inatividade

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `POST` | `/v1/agents/{id}/idle-actions` | Criar ação | `idle-actions:write` |
| `GET` | `/v1/agents/{id}/idle-actions` | Listar ações | `idle-actions:read` |
| `PUT` | `/v1/idle-actions/{id}` | Atualizar ação | `idle-actions:write` |
| `DELETE` | `/v1/idle-actions/{id}` | Deletar ação | `idle-actions:write` |

### 3.8 TRANSFER RULES — Regras de Transferência

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `POST` | `/v1/agents/{id}/transfer-rules` | Criar regra | `transfer-rules:write` |
| `GET` | `/v1/agents/{id}/transfer-rules` | Listar regras | `transfer-rules:read` |
| `PUT` | `/v1/transfer-rules/{id}` | Atualizar regra | `transfer-rules:write` |
| `DELETE` | `/v1/transfer-rules/{id}` | Deletar regra | `transfer-rules:write` |

### 3.9 MCP — Model Context Protocol

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `POST` | `/v1/agents/{id}/mcp` | Criar conexão MCP | `mcp:write` |
| `POST` | `/v1/mcp/{id}/connect` | Conectar MCP (OAuth) | `mcp:write` |
| `DELETE` | `/v1/mcp/{id}` | Deletar conexão | `mcp:write` |
| `GET` | `/v1/mcp/{id}/tools` | Listar tools | `mcp:read` |
| `POST` | `/v1/mcp/{id}/tools/{toolId}/activate` | Ativar tool | `mcp:write` |
| `POST` | `/v1/mcp/{id}/tools/{toolId}/deactivate` | Desativar tool | `mcp:write` |
| `POST` | `/v1/mcp/{id}/sync` | Sincronizar tools | `mcp:write` |

### 3.10 INTERACTIONS — Sessões de Atendimento

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `GET` | `/v1/interactions` | Listar interações | `interactions:read` |
| `GET` | `/v1/interactions/{id}/messages` | Mensagens da interação | `interactions:read` |
| `DELETE` | `/v1/interactions/{id}` | Deletar interação | `interactions:read` |

### 3.11 WORKSPACE — Gestão de Workspace

| Método | Path | Descrição | Scope |
|--------|------|-----------|-------|
| `GET` | `/v1/workspaces` | Listar workspaces | `workspaces:read` |
| `GET` | `/v1/workspaces/{id}/credits` | Saldo de créditos | `workspaces:read` |
| `GET` | `/v1/workspaces/{id}/agents` | Listar agentes do workspace | `workspaces:read` |

---

## 4. Estrutura de Epics e Stories

---

### EPIC 1: Agentes IA (Agents)
**Objetivo:** Permitir gerenciamento completo de agentes IA via API
**Prioridade:** P0 (Critical)
**Estimativa:** L (Large)

#### Stories:

**Story 1.1 — CRUD de Agentes**
> Como desenvolvedor, quero criar, listar, obter, atualizar e deletar agentes via API para automatizar o provisionamento de agentes.

- **Acceptance Criteria:**
  - `POST /v1/agents` cria agente com name, model, personality, behavior_rules
  - `GET /v1/agents` retorna lista paginada com filtro por status
  - `GET /v1/agents/{id}` retorna detalhes completos
  - `PUT /v1/agents/{id}` permite atualizar qualquer campo
  - `DELETE /v1/agents/{id}` remove agente (soft delete)
  - Todos requerem scope `agents:read` ou `agents:write`
  - Schema OpenAPI completo com exemplos
  - Documentação MDX no Mintlify

**Story 1.2 — Ativação/Desativação de Agentes**
> Como desenvolvedor, quero ativar ou desativar agentes via API para controlar quais agentes estão em operação.

- **Acceptance Criteria:**
  - `POST /v1/agents/{id}/activate` muda status para ativo
  - `POST /v1/agents/{id}/deactivate` muda status para inativo
  - Retorna o agente atualizado
  - Agente inativo não responde conversas

**Story 1.3 — Configurações do Agente (Settings)**
> Como desenvolvedor, quero gerenciar configurações avançadas do agente via API.

- **Acceptance Criteria:**
  - `GET /v1/agents/{id}/settings` retorna configurações (model, temperature, max_tokens, communication_style, response_format)
  - `PUT /v1/agents/{id}/settings` permite atualizar configurações
  - Validação de ranges (temperature 0-1, max_tokens limits)

**Story 1.4 — Webhooks do Agente**
> Como desenvolvedor, quero configurar webhooks para receber eventos do agente em tempo real.

- **Acceptance Criteria:**
  - `GET /v1/agents/{id}/webhooks` retorna webhooks configurados
  - `PUT /v1/agents/{id}/webhooks` permite configurar URLs, eventos, headers customizados
  - Suporte a eventos: `conversation.started`, `conversation.ended`, `message.received`, `handoff.requested`

**Story 1.5 — Conversar com Agente via API**
> Como desenvolvedor, quero enviar mensagens diretamente a um agente e receber respostas via API.

- **Acceptance Criteria:**
  - `POST /v1/agents/{id}/conversation` aceita text, image_url, audio_url
  - Suporta `conversation_id` para manter contexto
  - Retorna resposta do agente com tokens utilizados
  - Suporte a streaming via `Accept: text/event-stream` (SSE)

**Story 1.6 — Adicionar Contexto ao Agente**
> Como desenvolvedor, quero injetar contexto adicional em uma conversa do agente.

- **Acceptance Criteria:**
  - `POST /v1/agents/{id}/context` aceita `conversation_id`, `role`, `content`
  - Permite adicionar mensagens de sistema ou histórico

**Story 1.7 — Consumo de Créditos e Histórico**
> Como desenvolvedor, quero consultar o consumo de créditos e histórico de comportamento de um agente.

- **Acceptance Criteria:**
  - `GET /v1/agents/{id}/credits` retorna consumo por período (query params: `start_date`, `end_date`)
  - `GET /v1/agents/{id}/behavior-history` retorna log de mudanças de configuração

---

### EPIC 2: Treinamentos (Trainings)
**Objetivo:** Gerenciar treinamentos/knowledge base dos agentes via API
**Prioridade:** P0 (Critical)
**Estimativa:** M (Medium)

#### Stories:

**Story 2.1 — CRUD de Treinamentos**
> Como desenvolvedor, quero criar, listar, atualizar e deletar treinamentos de um agente via API.

- **Acceptance Criteria:**
  - `POST /v1/agents/{id}/trainings` aceita tipo (text, url, file) e conteúdo
  - `GET /v1/agents/{id}/trainings` lista treinamentos com status de processamento
  - `PUT /v1/trainings/{id}` atualiza apenas treinamentos de texto
  - `DELETE /v1/trainings/{id}` remove treinamento
  - Status do training: `processing`, `completed`, `failed`

---

### EPIC 3: Canais de Comunicação (Channels)
**Objetivo:** Permitir gerenciamento de canais (WhatsApp, Telegram, Widget, Email) via API
**Prioridade:** P0 (Critical)
**Estimativa:** L (Large)

#### Stories:

**Story 3.1 — CRUD de Canais**
> Como desenvolvedor, quero criar, listar, editar e remover canais de comunicação via API.

- **Acceptance Criteria:**
  - `POST /v1/channels` cria canal com type (whatsapp, telegram, email, website), agent_id
  - `GET /v1/channels` lista canais com filtro por type e status
  - `PUT /v1/channels/{id}` atualiza canal (nome, agente vinculado)
  - `DELETE /v1/channels/{id}` remove canal
  - Validação: tipo de canal válido, agente existente

**Story 3.2 — Configuração de Canal**
> Como desenvolvedor, quero gerenciar configurações específicas de cada canal.

- **Acceptance Criteria:**
  - `GET /v1/channels/{id}/config` retorna config específica por tipo
  - `PUT /v1/channels/{id}/config` atualiza configurações
  - Configs variam por tipo: WhatsApp (provider, number), Telegram (bot_token), Widget (colors, position)

**Story 3.3 — QR Code e Widget**
> Como desenvolvedor, quero obter QR codes para conexão WhatsApp e links de widget.

- **Acceptance Criteria:**
  - `GET /v1/channels/{id}/qr-code` retorna QR code como base64 ou URL
  - `GET /v1/channels/{id}/widget/links` retorna script tags para embed
  - `PUT /v1/channels/{id}/widget/settings` atualiza aparência do widget

**Story 3.4 — Iniciar Conversa por Canal**
> Como desenvolvedor, quero iniciar uma conversa programaticamente em um canal.

- **Acceptance Criteria:**
  - `POST /v1/channels/{id}/conversation` cria nova conversa no canal
  - Aceita `contact_id` ou dados do contato (nome, telefone, email)
  - Retorna `conversation_id` para acompanhamento

---

### EPIC 4: Chats e Mensagens (Expansão de Conversations)
**Objetivo:** Expandir funcionalidades de chat com envio de mensagens, handoff humano e gestão
**Prioridade:** P0 (Critical)
**Estimativa:** L (Large)

#### Stories:

**Story 4.1 — Envio e Gestão de Mensagens**
> Como desenvolvedor, quero enviar, editar e deletar mensagens em conversas via API.

- **Acceptance Criteria:**
  - `POST /v1/conversations/{id}/messages` envia mensagem (text, image, audio, document)
  - `PUT /v1/conversations/{id}/messages/{messageId}` edita mensagem (quando suportado pelo canal)
  - `DELETE /v1/conversations/{id}/messages/{messageId}` deleta mensagem individual
  - `DELETE /v1/conversations/{id}/messages` limpa todas as mensagens
  - Retorna status de entrega quando disponível

**Story 4.2 — Deletar Conversa**
> Como desenvolvedor, quero deletar conversas inteiras via API.

- **Acceptance Criteria:**
  - `DELETE /v1/conversations/{id}` remove conversa e mensagens associadas
  - Soft delete com possibilidade de auditoria
  - Retorna 204 No Content em sucesso

**Story 4.3 — Handoff Humano**
> Como desenvolvedor, quero controlar a transição entre atendimento IA e humano via API.

- **Acceptance Criteria:**
  - `POST /v1/conversations/{id}/human-handoff` pausa IA e habilita atendimento humano
  - `POST /v1/conversations/{id}/ai-resume` retoma atendimento IA
  - Campo `attendant_id` opcional para designar atendente
  - Evento de webhook disparado na transição

---

### EPIC 5: Campos Personalizados (Custom Fields)
**Objetivo:** Permitir criação e gestão de campos customizados no workspace
**Prioridade:** P1 (High)
**Estimativa:** S (Small)

#### Stories:

**Story 5.1 — CRUD de Campos Personalizados**
> Como desenvolvedor, quero criar e gerenciar campos personalizados para enriquecer dados de contatos e leads.

- **Acceptance Criteria:**
  - `POST /v1/custom-fields` cria campo com name, type (text, number, date, select, multi_select, boolean), options (para select)
  - `GET /v1/custom-fields` lista todos os campos com status
  - `PUT /v1/custom-fields/{id}` atualiza nome, opções
  - `PUT /v1/custom-fields/{id}/archive` toggle arquivar/desarquivar
  - Campos arquivados não aparecem em formulários mas mantêm dados

---

### EPIC 6: Intenções (Intentions)
**Objetivo:** Gerenciar ações de API/integrações que os agentes podem executar
**Prioridade:** P1 (High)
**Estimativa:** M (Medium)

#### Stories:

**Story 6.1 — CRUD de Intenções**
> Como desenvolvedor, quero criar intenções que permitem ao agente fazer chamadas API externas durante conversas.

- **Acceptance Criteria:**
  - `POST /v1/agents/{id}/intentions` cria intenção com name, description, trigger, action (HTTP method, URL, headers, body template)
  - `GET /v1/agents/{id}/intentions` lista intenções do agente
  - `PUT /v1/intentions/{id}` atualiza intenção
  - `DELETE /v1/intentions/{id}` remove intenção
  - Suporte a variáveis de template (`{{contact.name}}`, `{{message.content}}`)

---

### EPIC 7: Ações por Inatividade (Idle Actions)
**Objetivo:** Configurar ações automáticas quando conversas ficam inativas
**Prioridade:** P1 (High)
**Estimativa:** S (Small)

#### Stories:

**Story 7.1 — CRUD de Idle Actions**
> Como desenvolvedor, quero configurar ações automáticas para quando o cliente fica inativo na conversa.

- **Acceptance Criteria:**
  - `POST /v1/agents/{id}/idle-actions` cria ação com timeout_minutes, action_type (send_message, close_chat, transfer), message_template
  - `GET /v1/agents/{id}/idle-actions` lista ações
  - `PUT /v1/idle-actions/{id}` atualiza ação
  - `DELETE /v1/idle-actions/{id}` remove ação

---

### EPIC 8: Regras de Transferência (Transfer Rules)
**Objetivo:** Configurar quando e para quem o agente transfere a conversa
**Prioridade:** P1 (High)
**Estimativa:** S (Small)

#### Stories:

**Story 8.1 — CRUD de Transfer Rules**
> Como desenvolvedor, quero definir regras para transferência automática de conversas entre agentes ou para atendentes humanos.

- **Acceptance Criteria:**
  - `POST /v1/agents/{id}/transfer-rules` cria regra com condition (keyword, intent, sentiment), target_type (agent, human, team), target_id
  - `GET /v1/agents/{id}/transfer-rules` lista regras
  - `PUT /v1/transfer-rules/{id}` atualiza regra
  - `DELETE /v1/transfer-rules/{id}` remove regra

---

### EPIC 9: MCP — Model Context Protocol
**Objetivo:** Gerenciar conexões MCP e tools disponíveis para os agentes
**Prioridade:** P2 (Medium)
**Estimativa:** M (Medium)

#### Stories:

**Story 9.1 — Conexões MCP**
> Como desenvolvedor, quero gerenciar conexões MCP para expandir as capacidades dos agentes com tools externas.

- **Acceptance Criteria:**
  - `POST /v1/agents/{id}/mcp` cria conexão com name, server_url, transport_type (stdio, sse)
  - `POST /v1/mcp/{id}/connect` inicia conexão OAuth quando necessário
  - `DELETE /v1/mcp/{id}` remove conexão
  - Status de conexão: `connected`, `disconnected`, `error`

**Story 9.2 — Gestão de Tools MCP**
> Como desenvolvedor, quero listar e controlar quais tools MCP estão ativas para o agente.

- **Acceptance Criteria:**
  - `GET /v1/mcp/{id}/tools` lista tools disponíveis com status
  - `POST /v1/mcp/{id}/tools/{toolId}/activate` ativa tool
  - `POST /v1/mcp/{id}/tools/{toolId}/deactivate` desativa tool
  - `POST /v1/mcp/{id}/sync` sincroniza lista de tools com servidor MCP

---

### EPIC 10: Interações / Analytics (Interactions)
**Objetivo:** Acessar dados de sessões de atendimento para análise
**Prioridade:** P2 (Medium)
**Estimativa:** S (Small)

#### Stories:

**Story 10.1 — Consulta de Interações**
> Como desenvolvedor, quero acessar sessões de atendimento para analytics e relatórios.

- **Acceptance Criteria:**
  - `GET /v1/interactions` lista interações paginadas com filtros (date_range, channel, status, agent_id)
  - `GET /v1/interactions/{id}/messages` retorna mensagens da interação
  - `DELETE /v1/interactions/{id}` remove registro de interação
  - Inclui metadados: duration, message_count, satisfaction_score

---

### EPIC 11: Workspace
**Objetivo:** Consultar informações de workspace e créditos
**Prioridade:** P2 (Medium)
**Estimativa:** S (Small)

#### Stories:

**Story 11.1 — Consulta de Workspace e Créditos**
> Como desenvolvedor, quero consultar informações do workspace e saldo de créditos via API.

- **Acceptance Criteria:**
  - `GET /v1/workspaces` lista workspaces da conta
  - `GET /v1/workspaces/{id}/credits` retorna saldo atual e consumo
  - `GET /v1/workspaces/{id}/agents` lista agentes do workspace
  - Dados de crédito: balance, used, plan_limit, auto_recharge status

---

### EPIC 12: Documentação e Infraestrutura
**Objetivo:** Atualizar toda documentação OpenAPI e Mintlify
**Prioridade:** P0 (Critical)
**Estimativa:** L (Large)

#### Stories:

**Story 12.1 — Expandir OpenAPI Spec (openapi.json)**
> Como desenvolvedor, quero que o openapi.json contenha todos os novos endpoints com schemas completos.

- **Acceptance Criteria:**
  - Todos os ~60 novos endpoints documentados no OpenAPI 3.1.0
  - Schemas de request/response para cada operação
  - Exemplos de request e response
  - Descrições em português
  - Novos tags para cada grupo
  - Novos security scopes documentados

**Story 12.2 — Atualizar Sidebar do Mintlify (docs.json)**
> Como desenvolvedor, quero que o sidebar da documentação reflita todos os novos grupos de endpoints.

- **Acceptance Criteria:**
  - Novos groups no tab "API reference": Agents, Trainings, Channels, Chats, Custom Fields, Intentions, Idle Actions, Transfer Rules, MCP, Interactions, Workspace
  - Cada group lista todas as operações
  - Ordem lógica de navegação

**Story 12.3 — Atualizar Página de Introdução da API**
> Como desenvolvedor, quero que a introdução da API documente todos os novos scopes e recursos.

- **Acceptance Criteria:**
  - Tabela de scopes atualizada
  - Lista completa de error codes
  - Exemplos de autenticação atualizados
  - Guia de rate limiting
  - Seção de changelog com novos endpoints

**Story 12.4 — Criar Páginas de Guia para Novos Recursos**
> Como desenvolvedor, quero guias explicando como usar os novos endpoints em cenários práticos.

- **Acceptance Criteria:**
  - Guia: "Provisionando Agentes via API"
  - Guia: "Configurando Canais Programaticamente"
  - Guia: "Automação de Atendimento com Handoff"
  - Guia: "Expandindo Agentes com MCP"

---

## 5. Comparativo GPT Maker → Timely.ai

| GPT Maker (v2) | Timely.ai (v1) | Status |
|----------------|----------------|--------|
| `POST /v2/workspace/{id}/agents` | `POST /v1/agents` | NOVO |
| `GET /v2/agent/{id}` | `GET /v1/agents/{id}` | NOVO |
| `PUT /v2/agent/{id}` | `PUT /v1/agents/{id}` | NOVO |
| `DELETE /v2/agent/{id}` | `DELETE /v1/agents/{id}` | NOVO |
| `PUT /v2/agent/{id}/active` | `POST /v1/agents/{id}/activate` | NOVO |
| `PUT /v2/agent/{id}/inactive` | `POST /v1/agents/{id}/deactivate` | NOVO |
| `GET /v2/agent/{id}/settings` | `GET /v1/agents/{id}/settings` | NOVO |
| `PUT /v2/agent/{id}/settings` | `PUT /v1/agents/{id}/settings` | NOVO |
| `POST /v2/agent/{id}/conversation` | `POST /v1/agents/{id}/conversation` | NOVO |
| `POST /v2/agent/{id}/add-message` | `POST /v1/agents/{id}/context` | NOVO |
| `GET /v2/agent/{id}/trainings` | `GET /v1/agents/{id}/trainings` | NOVO |
| `POST /v2/agent/{id}/trainings` | `POST /v1/agents/{id}/trainings` | NOVO |
| `PUT /v2/training/{id}` | `PUT /v1/trainings/{id}` | NOVO |
| `DELETE /v2/training/{id}` | `DELETE /v1/trainings/{id}` | NOVO |
| `GET /v2/agent/{id}/webhooks` | `GET /v1/agents/{id}/webhooks` | NOVO |
| `PUT /v2/agent/{id}/webhooks` | `PUT /v1/agents/{id}/webhooks` | NOVO |
| `GET /v2/agent/{id}/list-behavior-history` | `GET /v1/agents/{id}/behavior-history` | NOVO |
| `GET /v2/agent/{id}/credits-spent` | `GET /v1/agents/{id}/credits` | NOVO |
| `POST /v2/agent/{id}/create-channel` | `POST /v1/channels` | NOVO |
| `GET /v2/workspace/{id}/channels` | `GET /v1/channels` | NOVO |
| `PUT /v2/channel/{id}` | `PUT /v1/channels/{id}` | NOVO |
| `DELETE /v2/channel/{id}` | `DELETE /v1/channels/{id}` | NOVO |
| `GET /v2/channel/{id}/config` | `GET /v1/channels/{id}/config` | NOVO |
| `PUT /v2/channel/{id}/config` | `PUT /v1/channels/{id}/config` | NOVO |
| `GET /v2/channel/{id}/qr-code` | `GET /v1/channels/{id}/qr-code` | NOVO |
| `POST /v2/channel/{id}/start-conversation` | `POST /v1/channels/{id}/conversation` | NOVO |
| `GET /v2/channel/{id}/widget-links` | `GET /v1/channels/{id}/widget/links` | NOVO |
| `PUT /v2/channel/{id}/widget-settings` | `PUT /v1/channels/{id}/widget/settings` | NOVO |
| `GET /v2/workspace/{id}/chats` | `GET /v1/conversations` | EXISTE |
| `GET /v2/chat/{id}/messages` | `GET /v1/conversations/{id}/messages` | EXISTE |
| `POST /v2/chat/{id}/send-message` | `POST /v1/conversations/{id}/messages` | NOVO |
| `PUT /v2/chat/{id}/message/{mid}` | `PUT /v1/conversations/{id}/messages/{mid}` | NOVO |
| `DELETE /v2/chat/{id}/message/{mid}` | `DELETE /v1/conversations/{id}/messages/{mid}` | NOVO |
| `DELETE /v2/chat/{id}/messages` | `DELETE /v1/conversations/{id}/messages` | NOVO |
| `DELETE /v2/chat/{id}` | `DELETE /v1/conversations/{id}` | NOVO |
| `PUT /v2/chat/{id}/start-human` | `POST /v1/conversations/{id}/human-handoff` | NOVO |
| `PUT /v2/chat/{id}/stop-human` | `POST /v1/conversations/{id}/ai-resume` | NOVO |
| `GET /v2/workspace/{id}/contact/{id}` | `GET /v1/contacts/{id}` | EXISTE |
| `GET /v2/workspace/{id}/search` | `GET /v1/contacts` | EXISTE |
| `PUT /v2/contact/{id}/update` | `PUT /v1/contacts/{id}` | EXISTE |
| `POST /v2/custom-field/workspace/{id}` | `POST /v1/custom-fields` | NOVO |
| `GET /v2/custom-field/workspace/{id}` | `GET /v1/custom-fields` | NOVO |
| `PUT /v2/custom-field/{id}` | `PUT /v1/custom-fields/{id}` | NOVO |
| `PUT /v2/custom-field/toggle-archive/{id}` | `PUT /v1/custom-fields/{id}/archive` | NOVO |
| `POST /v2/agent/{id}/intentions` | `POST /v1/agents/{id}/intentions` | NOVO |
| `GET /v2/agent/{id}/intentions` | `GET /v1/agents/{id}/intentions` | NOVO |
| `PUT /v2/intention/{id}` | `PUT /v1/intentions/{id}` | NOVO |
| `DELETE /v2/intention/{id}` | `DELETE /v1/intentions/{id}` | NOVO |
| `POST /v2/agent/{id}/idle-actions` | `POST /v1/agents/{id}/idle-actions` | NOVO |
| `GET /v2/agent/{id}/idle-actions` | `GET /v1/agents/{id}/idle-actions` | NOVO |
| `PUT /v2/agent/{id}/idle-actions` | `PUT /v1/idle-actions/{id}` | NOVO |
| `DELETE /v2/agent/{id}/idle-actions` | `DELETE /v1/idle-actions/{id}` | NOVO |
| `POST /v2/agent/{id}/transfer-rules` | `POST /v1/agents/{id}/transfer-rules` | NOVO |
| `GET /v2/agent/{id}/transfer-rules` | `GET /v1/agents/{id}/transfer-rules` | NOVO |
| `PUT /v2/agent/{id}/transfer-rules/{id}` | `PUT /v1/transfer-rules/{id}` | NOVO |
| `DELETE /v2/agent/{id}/transfer-rules/{id}` | `DELETE /v1/transfer-rules/{id}` | NOVO |
| `POST /v2/agent/{id}/mcp/add` | `POST /v1/agents/{id}/mcp` | NOVO |
| `POST /v2/mcp/connect` | `POST /v1/mcp/{id}/connect` | NOVO |
| `DELETE /v2/mcp/{id}` | `DELETE /v1/mcp/{id}` | NOVO |
| `GET /v2/mcp/{id}/tools` | `GET /v1/mcp/{id}/tools` | NOVO |
| `GET /v2/mcp/{id}/tool/{tid}/active` | `POST /v1/mcp/{id}/tools/{tid}/activate` | NOVO |
| `GET /v2/mcp/{id}/tool/{tid}/inactive` | `POST /v1/mcp/{id}/tools/{tid}/deactivate` | NOVO |
| `GET /v2/mcp/{id}/sync-tools` | `POST /v1/mcp/{id}/sync` | NOVO |
| `GET /v2/workspace/{id}/interactions` | `GET /v1/interactions` | NOVO |
| `GET /v2/interaction/{id}/messages` | `GET /v1/interactions/{id}/messages` | NOVO |
| `DELETE /v2/interaction/{id}` | `DELETE /v1/interactions/{id}` | NOVO |
| `GET /v2/workspaces` | `GET /v1/workspaces` | NOVO |
| `GET /v2/workspace/{id}/credits` | `GET /v1/workspaces/{id}/credits` | NOVO |
| `GET /v2/workspace/{id}/agents` | `GET /v1/workspaces/{id}/agents` | NOVO |

**Total: ~65 novos endpoints + 7 expansões em existentes**

---

## 6. Plano de Implementação por Waves

### Wave 1 — Core (P0)
1. Epic 1: Agents (15 endpoints)
2. Epic 2: Trainings (4 endpoints)
3. Epic 3: Channels (10 endpoints)
4. Epic 4: Chats expansion (7 endpoints)
5. Epic 12: Documentação OpenAPI + Mintlify

### Wave 2 — Enhancements (P1)
6. Epic 5: Custom Fields (4 endpoints)
7. Epic 6: Intentions (4 endpoints)
8. Epic 7: Idle Actions (4 endpoints)
9. Epic 8: Transfer Rules (4 endpoints)

### Wave 3 — Advanced (P2)
10. Epic 9: MCP (7 endpoints)
11. Epic 10: Interactions (3 endpoints)
12. Epic 11: Workspace (3 endpoints)

---

## 7. Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Breaking changes nos endpoints existentes | Alto | Manter 100% backward compatibility, novos endpoints apenas |
| Inconsistência de schemas | Médio | Reusar patterns existentes (Pagination, Error, etc.) |
| Scopes muito granulares | Baixo | Agrupar scopes logicamente, documentar claramente |
| Rate limiting insuficiente | Médio | Monitorar uso e ajustar limites por endpoint |
| Documentação desatualizada | Alto | Gerar docs a partir do OpenAPI, single source of truth |

---

## 8. Definição de Pronto (Definition of Done)

Para cada endpoint:
- [ ] Schema definido no `openapi.json`
- [ ] Endpoint listado no `docs.json` (sidebar)
- [ ] Exemplos de request/response no schema
- [ ] Descrições em português
- [ ] Scopes de autorização documentados
- [ ] Error responses mapeados
- [ ] Build do Mintlify sem erros

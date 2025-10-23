E 

---

# 🧠 **Product Requirements Document (PRD) – RuvScan MCP**

### **Version:** v0.2 (Generalized MVP)

### **Owner:** Colm Byrne (Flout Labs)

### **Date:** October 2025

### **Tagline:**

> “RuvScan: The MCP that finds leverage you didn’t know existed — anywhere on GitHub.”

---

## 1. 🎯 Product Summary

**RuvScan** is an **MCP-compliant intelligence discovery server** that continuously scans selected GitHub repositories or organizations and transforms their READMEs into structured, queryable *Leverage Cards*.

Unlike keyword search, RuvScan performs **conceptual reasoning** to identify *non-obvious reuse opportunities* between what you’re building and what already exists elsewhere.

---

## 2. 🧩 Problem Statement

Developers and product builders waste time reinventing existing tools, libraries, and ideas because:

* GitHub discovery is keyword-based, not conceptual.
* Existing recommendation systems surface *similar* projects, not *complementary* ones.
* The “outside-the-box” mapping between a repo’s purpose and your intent is invisible.

**RuvScan** turns this invisible layer visible — an *MCP scout agent* that constantly asks:

> “What’s already out there that could 10× what you’re doing right now?”

---

## 3. 💡 Product Goals

### ✅ **Primary Goals**

1. **Scan any GitHub source**

   * Organization (e.g., `ruvnet`), user, topic, or list of repos.
   * Parse metadata and README.md content.
2. **Summarize each repo into a structured Leverage Card**

   * Core capabilities
   * Tech stack
   * Non-obvious leverage (“how else could this be used?”)
3. **Expose results through a local MCP server**

   * `/scan` → triggers or schedules scanning
   * `/query` → accepts natural-language intents
   * `/cards` → returns stored summaries
4. **Support “outside-the-box” reasoning**

   * Uses an LLM to infer potential secondary or abstract uses.

### 🚫 **Non-Goals**

* Full code-base analysis (beyond README / metadata).
* UI/UX dashboard (MVP is CLI + MCP only).
* Automated pull-request generation or code modification.

---

## 4. 🧠 Core User Stories

| # | User Story                                                                              | Acceptance Criteria                                    |
| - | --------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 1 | As a builder, I want to **point RuvScan to any GitHub org or repo list**                | Config supports `target: org`, `user`, or `repo-list`  |
| 2 | As a user, I want to **scan repos and summarize them**                                  | `/scan` parses ≥50 repos and stores structured JSON    |
| 3 | As a builder, I want to **ask questions like “what could optimize my context recall?”** | `/query` returns ranked Leverage Cards with rationales |
| 4 | As a developer, I want to **run RuvScan locally via MCP**                               | `ruvscan serve` spins up FastAPI MCP server            |
| 5 | As a team, I want **periodic auto-scan + diff detection**                               | Scheduler detects new/updated repos and updates index  |

---

## 5. ⚙️ Functional Requirements

### **Endpoints**

| Endpoint  | Method   | Description                                       |
| --------- | -------- | ------------------------------------------------- |
| `/scan`   | POST     | Scan configured targets (org, user, or repo list) |
| `/query`  | POST     | Query intent (“speed up parsing”) → get matches   |
| `/cards`  | GET      | List stored Leverage Cards                        |
| `/config` | GET/POST | Manage targets and scanning schedule              |
| `/health` | GET      | System status                                     |

### **Configuration Example**

```yaml
targets:
  - type: org
    name: ruvnet
  - type: user
    name: floutlabs
  - type: topic
    name: agentic-ai
scan_frequency: daily
storage: sqlite
mcp:
  port: 8081
```

---

## 6. 📦 Leverage Card Schema

```json
{
  "repo": "github.com/org/repo",
  "summary": "Sublinear-time solver for asymmetric systems.",
  "capabilities": ["solver", "optimization", "pattern search"],
  "languages": ["Rust"],
  "outside_box_reasoning": "Could replace regex scanning in HubDuck for 8x speed.",
  "integration_hint": "Expose via WASM binding for frontend inference.",
  "relevance_score": 0.91,
  "last_updated": "2025-10-23T10:00Z"
}
```

---

## 7. 🏗️ System Architecture (MVP)

```
        +-------------------------+
        |        CLI / IDE        |
        +-----------+-------------+
                    |
                    v
          +---------+----------+
          |     RuvScan MCP    |
          |  (FastAPI Server)  |
          +---------+----------+
                    |
         +----------+----------+
         |  Summarizer Agent   |
         | (LLM reasoning)     |
         +----------+----------+
                    |
         +----------+----------+
         |  Scanner Agent      |
         | (GitHub API fetch)  |
         +----------+----------+
                    |
         +----------+----------+
         |  Local DB (SQLite)  |
         +---------------------+
```

* **Scanner**: pulls repo names + READMEs via GitHub GraphQL API.
* **Summarizer**: LLM generates Leverage Cards (JSON).
* **Storage**: lightweight DB (SQLite or Supabase).
* **MCP Server**: exposes query + scan endpoints for external tools.
* **Client**: IDE plugin or CLI querying `/query`.

---

## 8. 🧱 Technical Stack

| Component  | Technology                   |
| ---------- | ---------------------------- |
| Language   | Python 3.11                  |
| Framework  | FastAPI                      |
| DB         | SQLite / Supabase            |
| Model      | OpenAI GPT-4o-mini           |
| Scheduler  | APScheduler                  |
| API Access | GitHub GraphQL API           |
| Protocol   | Model Context Protocol (MCP) |

---

## 9. 📈 Success Metrics

| Metric              | Target                 |
| ------------------- | ---------------------- |
| Setup Time          | <5 min                 |
| Scan Coverage       | ≥80% of listed repos   |
| Useful Insight Rate | ≥70% judged “valuable” |
| Avg Query Latency   | <3 seconds             |
| Mean Card Freshness | ≤24 hours old          |

---

## 10. 🗓️ MVP Timeline

| Week       | Deliverable                              |
| ---------- | ---------------------------------------- |
| **Week 1** | FastAPI skeleton + MCP adapter           |
| **Week 2** | GitHub scanner + README parser           |
| **Week 3** | LLM summarizer → Leverage Card generator |
| **Week 4** | `/query` endpoint + intent reasoning     |
| **Week 5** | SQLite persistence + scheduler           |
| **Week 6** | CLI + local test suite                   |

---

## 11. 🔮 Future Extensions

| Feature                 | Description                                                     |
| ----------------------- | --------------------------------------------------------------- |
| Multi-Repo Intelligence | Scan multiple ecosystems (OpenAI, HuggingFace, Anthropic, etc.) |
| Contextual Adapter      | Learn from your local projects to weight relevance              |
| Deep Semantic Links     | Build a “Concept Graph” connecting related capabilities         |
| Team Federation         | Share findings between builders via Supabase sync               |
| Auto-Prototype Mode     | Suggest code snippets to integrate discovered leverage          |

---

## 12. ⚡ Example Query Flow

**User (CLI):**

```bash
ruvscan query "find libraries to visualize agent reasoning"
```

**MCP Response:**

```json
{
  "repo": "github.com/ruvnet/infinity-ui",
  "summary": "Sci-fi inspired interface for agentic visualization.",
  "outside_box_reasoning": "Could serve as a debugging lens for agent clusters in AMP.",
  "integration_hint": "Use as front-end visualization template.",
  "relevance_score": 0.88
}
```

---

✅ **In short:**
RuvScan becomes your *contextual, cross-repo intelligence layer*.
It’s simple, open, and generalizable — a **local MCP that helps any builder think laterally across GitHub’s collective mind.**

---

Would you like me to now create the **project folder structure + FastAPI/MCP stub code** so you can drop it into Cursor or Replit to begin the MVP?


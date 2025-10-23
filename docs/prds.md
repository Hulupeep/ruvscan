 

This version trims everything to its **minimum viable form** while retaining the essence: a hybrid MCP agent that uses **Ruvnet’s sublinear intelligence stack** to find *outside-the-box leverage* across GitHub.

---

# 🧠 **Product Requirements Document (PRD) — RuvScan MVP**

**Version:** v0.5 (MVP Scope)
**Owner:** Colm Byrne (Flout Labs)
**Date:** October 2025
**Product Type:** MCP Intelligence Server
**Tagline:**

> “RuvScan: The sublinear intelligence layer that finds the world’s hidden leverage.”

---

## 1. 🎯 **Purpose**

RuvScan is an **MCP-compatible AI service** that scans GitHub repositories and surfaces *non-obvious leverage* — ideas, tools, or frameworks that can accelerate a user’s build.

It doesn’t just search by keywords; it **thinks conceptually** using Ruvnet’s own sublinear, emergent, and deterministic frameworks (`sublinear-time-solver`, `FACT`, `MidStream`, `SAFLA`).

The MVP’s goal: **prove that RuvScan can scan, summarize, and reason about open-source projects in real-time** and deliver useful, creative leverage suggestions.

---

## 2. 🧩 **Problem**

Builders and product teams are buried under billions of open-source projects but can’t see:

* What *existing* code or idea could 10× their project.
* Which repos solve problems in *different but applicable* domains.
* How to reuse or adapt them quickly.

Traditional GitHub search is linear, literal, and blind to conceptual analogy.
**RuvScan’s advantage:** it uses *sublinear algorithms* to search *semantically and analogically* — surfacing reuse opportunities that normal search misses.

---

## 3. 🚀 **MVP Goals**

| Goal                           | Description                                                                                   | Success Metric                     |
| ------------------------------ | --------------------------------------------------------------------------------------------- | ---------------------------------- |
| **Scan GitHub Repos**          | Fetch and summarize repos (by org or topic).                                                  | ≥50 repos scanned per run          |
| **Sublinear Similarity**       | Compute conceptual proximity between repos and user intent using the `sublinear-time-solver`. | O(log n) compute; <3 s per query   |
| **Reasoning Layer**            | Generate outside-the-box reuse ideas with deterministic caching (`FACT`).                     | ≥70% rated “useful” by testers     |
| **Serve via MCP**              | Respond to `/scan` and `/query` endpoints.                                                    | JSON output in standard MCP format |
| **Store Reproducible Context** | Log reasoning chain and summaries locally.                                                    | 100% deterministic replay via FACT |

---

## 4. 🧱 **MVP Scope**

### ✅ **In Scope**

* One-click scan of GitHub org/user/topic.
* README summarization (LLM-based).
* Sublinear similarity computation via Rust engine.
* Generation of *Leverage Cards* (concept + reuse rationale).
* Local cache using FACT.
* Simple MCP API (`/scan`, `/query`, `/cards`).

### 🚫 **Out of Scope (for MVP)**

* Deep source code parsing (beyond README).
* Federated or distributed mode.
* Real-time streaming updates (MidStream integration is Phase 2).
* Full Go worker clustering (use single-thread fetcher).

---

## 5. 🧠 **Core User Story**

> As a builder, I want to query RuvScan with what I’m working on and instantly see which GitHub projects could accelerate or inspire my build — even if they weren’t made for my domain.

**Example:**

> “I’m building a context memory system for my AI app. What can I reuse?”

**RuvScan Response (MCP JSON):**

```json
{
  "repo": "ruvnet/FACT",
  "summary": "Deterministic caching layer for prompt replay and reproducible reasoning.",
  "outside_box_reasoning": "Could serve as the memory backbone for your AI context system, replacing ephemeral vector caches.",
  "integration_hint": "Embed FACT as a local MCP tool to persist context states.",
  "relevance_score": 0.91
}
```

---

## 6. ⚙️ **Functional Requirements**

| Feature         | Description                                                                  |
| --------------- | ---------------------------------------------------------------------------- |
| **/scan**       | Pulls all repos from configured GitHub org/topic.                            |
| **/query**      | Accepts intent text; finds matching leverage using sublinear similarity.     |
| **/cards**      | Returns stored leverage results (with timestamps).                           |
| **FACT Cache**  | Saves deterministic reasoning chain and replay data.                         |
| **Rust Bridge** | Performs O(log n) vector similarity comparisons via `sublinear-time-solver`. |

---

## 7. 🧩 **System Architecture (MVP Simplified)**

```
User / IDE / TabStax
        │
        ▼
🐍 Python MCP Server (FastAPI)
  ├── Summarize repos (LLM)
  ├── Store results (SQLite + FACT)
  ├── Query intent → vectorize → send to Rust
  └── Return ranked Leverage Cards
        │
        ▼
🦀 Rust Sublinear Engine (WASM)
  ├── Compute semantic similarity
  └── Return sorted matches
```

---

## 8. 💻 **Technical Stack (MVP)**

| Layer        | Technology                                    |
| ------------ | --------------------------------------------- |
| Orchestrator | Python 3.11 + FastAPI                         |
| AI/LLM       | GPT-4o-mini or local model                    |
| Cache        | FACT (prompt + reasoning replay)              |
| Engine       | Rust (`sublinear-time-solver` + WASM binding) |
| Storage      | SQLite                                        |
| Integration  | MCP (JSON-over-HTTP)                          |

---

## 9. ⚡ **Performance Targets**

| Metric               | Goal                                   |
| -------------------- | -------------------------------------- |
| Repos per scan       | ≥ 50                                   |
| Query latency        | ≤ 3 seconds                            |
| CPU usage            | ≤ 1 core                               |
| Memory footprint     | ≤ 500 MB                               |
| Deterministic replay | 100% (FACT validation)                 |
| User satisfaction    | ≥ 70% of test queries rated “valuable” |

---

## 10. 📈 **MVP Development Plan**

| Week  | Deliverable                                               |
| ----- | --------------------------------------------------------- |
| **1** | Setup FastAPI MCP skeleton + `/scan` + `/query` endpoints |
| **2** | Integrate GitHub API fetcher + README summarizer          |
| **3** | Add Rust sublinear engine (via PyO3 or WASM binding)      |
| **4** | Implement FACT cache + Leverage Card schema               |
| **5** | Test reasoning output + sample use cases                  |
| **6** | CLI + basic UX polish + documentation                     |

---

## 11. 🧮 **Leverage Card Schema**

```json
{
  "repo": "github.com/org/repo",
  "capabilities": ["solver", "context management"],
  "summary": "Short description of repo’s value.",
  "outside_box_reasoning": "Creative reuse idea.",
  "integration_hint": "How to connect or adapt.",
  "relevance_score": 0.0–1.0,
  "cached": true
}
```

---

## 12. 🧠 **Reasoning Design**

RuvScan’s “outside-the-box” suggestions come from a *two-pass process*:

1. **Literal Match:** Compare embeddings (sublinear-time-solver).
2. **Analogical Pass:** SAFLA agent interprets the top N results and generates conceptual analogies (e.g., “sublinear algorithms → real-time context retrieval”).

Both passes are cached by FACT, producing deterministic and reproducible creative reasoning.

---

## 13. 🔮 **Post-MVP Extensions**

| Phase    | Feature               | Description                                          |
| -------- | --------------------- | ---------------------------------------------------- |
| **v0.6** | Add Go scanner        | Asynchronous multi-threaded GitHub ingestion.        |
| **v0.7** | MidStream integration | Real-time scanning + inflight updates.               |
| **v0.8** | Supabase sync         | Cloud cache & multi-agent collaboration.             |
| **v1.0** | Self-optimizing agent | RuvScan learns which discoveries lead to real reuse. |

---

## 14. 🧭 **Optimum User Outcome**

* The user can **point RuvScan at any GitHub space** and ask a simple, natural-language question like *“what can 10× this idea?”*
* Within seconds, RuvScan returns **intelligent leverage suggestions**, backed by reproducible reasoning and sublinear compute.
* It feels less like a search engine — and more like a **creative co-researcher** that sees hidden structure across the world’s code.

---

## ✅ **MVP Success Definition**

> The MVP is successful when a single-user instance of RuvScan can:
>
> 1. Scan a GitHub org/topic and summarize ≥ 50 repos.
> 2. Accept a text intent query and return ranked, reasoned leverage cards within 3 seconds.
> 3. Reproduce identical reasoning outputs using FACT cache.
> 4. Demonstrate at least one **outside-domain reuse insight** that a human tester finds valuable.

---

Would you like me to now create the **project folder layout + starter code stubs** (Python FastAPI MCP, Rust solver binding, and SQLite schema) for the MVP phase so it’s ready to open in Cursor or Replit?


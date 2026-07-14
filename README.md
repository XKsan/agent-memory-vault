# Agent Memory Vault

A lightweight memory layer for AI agents.

Give your AI agents persistent memory without complex infrastructure.

---

## Why Agent Memory Vault?

Today's AI agents have a critical limitation:

They forget.

Every new conversation starts from zero.

Agent Memory Vault provides a simple local memory system that allows AI agents to remember:

- User preferences
- Project context
- Important decisions
- Workflow instructions
- Long-term knowledge

---

## Features

### Persistent Memory

Store important information permanently.

```python
vault.save(
    "user",
    "User prefers concise technical explanations."
)

import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from agent_memory import AgentMemoryVault


vault = AgentMemoryVault()


# Save user preferences
vault.save(
    "user",
    "User likes concise answers and practical solutions."
)


# Save project knowledge
vault.save(
    "project",
    "The product is building AI tools for independent creators."
)


# Retrieve relevant memory
context = vault.context("AI")


print("Agent Context:")
print(context)

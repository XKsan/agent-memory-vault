import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from agent_memory import AgentMemoryVault


vault = AgentMemoryVault()


vault.save("user", "User likes concise answers.", tags=["preference"])
vault.save("project", "CASH ENGINE builds AI products.", tags=["cash-engine"])

print(vault.stats())
print(vault.context("AI"))
print(vault.search("AI"))

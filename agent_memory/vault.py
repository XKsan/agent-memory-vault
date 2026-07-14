import os
import json
from datetime import datetime


class AgentMemoryVault:

    def __init__(self, path="memory"):
        self.path = path

        if not os.path.exists(self.path):
            os.makedirs(self.path)


    def save(self, category, content):

        filename = os.path.join(
            self.path,
            f"{category}.json"
        )

        data = []

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)


        memory = {
            "content": content,
            "created_at": datetime.now().isoformat()
        }


        if content not in [m["content"] for m in data]:
            data.append(memory)


        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )


        return memory



    def search(self, keyword):

        results = []

        for file in os.listdir(self.path):

            if file.endswith(".json"):

                filepath = os.path.join(
                    self.path,
                    file
                )


                with open(filepath, "r", encoding="utf-8") as f:
                    memories = json.load(f)


                for item in memories:

                    if keyword.lower() in item["content"].lower():
                        results.append(item)


        return results



    def context(self, keyword):

        memories = self.search(keyword)

        return "\n".join(
            [
                "- " + m["content"]
                for m in memories
            ]
        )



if __name__ == "__main__":

    vault = AgentMemoryVault()


    vault.save(
        "user",
        "User prefers concise technical explanations."
    )


    vault.save(
        "project",
        "CASH ENGINE builds small AI products daily."
    )


    print(
        vault.context("AI")
    )

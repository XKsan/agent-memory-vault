import os
import json
from datetime import datetime


class AgentMemoryVault:

    def __init__(self, path="memory"):
        self.path = path
        os.makedirs(self.path, exist_ok=True)

    def _file(self, category):
        return os.path.join(self.path, f"{category}.json")

    def _load(self, category):
        filename = self._file(category)

        if not os.path.exists(filename):
            return []

        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, category, data):

        with open(self._file(category), "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )

    def save(self, category, content, tags=None):

        data = self._load(category)

        for item in data:

            if item["content"] == content:

                item["last_access"] = datetime.now().isoformat()
                item["access_count"] += 1

                self._save(category, data)
                return item

        memory = {
            "content": content,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": None,
            "last_access": datetime.now().isoformat(),
            "access_count": 1
        }

        data.append(memory)

        self._save(category, data)

        return memory

    def list(self):

        result = {}

        for file in os.listdir(self.path):

            if file.endswith(".json"):

                category = file[:-5]

                result[category] = self._load(category)

        return result

    def categories(self):

        return [
            f[:-5]
            for f in os.listdir(self.path)
            if f.endswith(".json")
        ]

    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        for category in self.categories():

            data = self._load(category)

            changed = False

            for item in data:

                score = 0

                if keyword in item["content"].lower():
                    score += 10

                for tag in item.get("tags", []):

                    if keyword in tag.lower():
                        score += 5

                if score > 0:

                    item["last_access"] = datetime.now().isoformat()
                    item["access_count"] += 1

                    changed = True

                    results.append({
                        "category": category,
                        "score": score,
                        **item
                    })

            if changed:
                self._save(category, data)

        results.sort(
            key=lambda x: (
                x["score"],
                x["access_count"]
            ),
            reverse=True
        )

        return results

    def context(self, keyword):

        return "\n".join(
            f"- {m['content']}"
            for m in self.search(keyword)
        )

    def update(self, category, old_content, new_content):

        data = self._load(category)

        for item in data:

            if item["content"] == old_content:

                item["content"] = new_content
                item["updated_at"] = datetime.now().isoformat()

                self._save(category, data)

                return True

        return False

    def delete(self, category, content):

        data = self._load(category)

        new_data = [
            x
            for x in data
            if x["content"] != content
        ]

        self._save(category, new_data)

        return len(data) != len(new_data)

    def clear(self):

        for category in self.categories():

            os.remove(self._file(category))

    def export_json(self, filename):

        with open(filename, "w", encoding="utf-8") as f:

            json.dump(
                self.list(),
                f,
                indent=2,
                ensure_ascii=False
            )

    def import_json(self, filename):

        with open(filename, "r", encoding="utf-8") as f:

            data = json.load(f)

        for category, memories in data.items():

            self._save(category, memories)

    def stats(self):

        total = 0

        for category in self.categories():

            total += len(self._load(category))

        return {
            "categories": len(self.categories()),
            "memories": total
        }


if __name__ == "__main__":

    vault = AgentMemoryVault()

    vault.save(
        "user",
        "User likes concise answers.",
        tags=["preference"]
    )

    vault.save(
        "project",
        "CASH ENGINE builds AI products.",
        tags=["cash-engine"]
    )

    print(vault.context("AI"))

    print(vault.stats())
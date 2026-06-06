import json


class MetadataManager:

    def save(
        self,
        metadata,
        path
    ):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

    def load(self, path):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)
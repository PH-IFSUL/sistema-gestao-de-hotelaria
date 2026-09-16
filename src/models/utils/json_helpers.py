import json, os
from pathlib import Path
from typing import Any

class JSONHelper:

    """ @staticmethod
    def save_to_json(data: Any, file_path: str) -> None:
        
        Save data to a JSON file.

        :param data: Data to be saved (dict or list).
        :param file_path: Path to the JSON file.
       
        # testa se a pasta existe, se não existir cria a pasta
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Lê o arquivo JSON existente, se houver, e atualiza com os novos dados
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
                existing_data.update(data)
        except FileNotFoundError:
            existing_data = data

        # Save the updated data
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
 """
    @staticmethod
    def load_from_json(file_path: str) -> Any:
        """
        Load data from a JSON file.

        :param file_path: Path to the JSON file.
        :return: Data loaded from the JSON file (dict or list), None if empty.
        """
        if os.path.exists(file_path) and os.path.getsize(file_path) != 0:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return None
    
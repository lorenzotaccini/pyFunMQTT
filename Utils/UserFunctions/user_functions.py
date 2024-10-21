import base64
from abc import ABC, abstractmethod
from typing import Any
import io
from PIL import Image


class Service(ABC):
    @abstractmethod
    def serve(self, params: list, data: Any) -> Any:
        ...


# USER DEFINED CLASSES

class RemoveWS(Service):
    def serve(self, params, data: str):
        return data.replace(' ', '')


class Upper(Service):
    def serve(self, params, data: str):
        return str(data).upper()


class SplitCols(Service):
    """
    Divide una tabella (lista di dizionari) in n parti, suddividendo le colonne.

    Args:
    - table (list of dict): La tabella originale da dividere.
    - n (int): Il numero di parti in cui dividere la tabella.

    Returns:
    - list of list of dict: Una lista contenente n tabelle suddivise per colonne.
    """
    def serve(self, params: list, data: list) -> Any:
        n = params[0]
        # Estrai tutte le chiavi (colonne) dalla prima riga
        keys = list(data[0].keys())

        # Calcola il numero di colonne per ciascuna sottotabella
        total_columns = len(keys)
        avg_columns = total_columns // n
        remainder = total_columns % n

        # Lista per contenere le sottotabelle
        sub_tables = [[] for _ in range(n)]

        # Inizializza gli indici di partenza e fine per le colonne
        start_index = 0

        for i in range(n):
            # Calcola la lunghezza della sottotabella corrente
            end_index = start_index + avg_columns + (1 if i < remainder else 0)

            # Seleziona le colonne per la sottotabella corrente
            current_keys = keys[start_index:end_index]

            # Costruisce la sottotabella corrente con solo le colonne selezionate
            for row in data:
                sub_table_row = {key: row[key] for key in current_keys}
                sub_tables[i].append(sub_table_row)

            # Aggiorna l'indice di partenza per la prossima iterazione
            start_index = end_index

        print(sub_tables)
        return sub_tables


class SplitRows(Service):
    def serve(self, params: list, data: list) -> Any:
        n = params[0]

        total_rows = len(data)
        avg_rows = total_rows // n
        remainder = total_rows % n

        sub_tables = []

        start_index = 0

        for i in range(n):
            end_index = start_index + avg_rows + (1 if i < remainder else 0)
            current_rows = data[start_index:end_index]
            sub_tables.append(current_rows)
            start_index = end_index

        print(sub_tables)
        return sub_tables


class ExtractCols(Service):
    def serve(self, params: list, data: Any) -> Any:
        columns = list(data[0].keys())
        filtered_columns = [columns[i] for i in params if i < len(columns)]
        filtered_data = [
            [
                {key: row[key] for key in filtered_columns} for row in data
            ]
        ]
        print(filtered_data)
        return filtered_data


class ImageSplit(Service):

    def serve(self, params: list, data: bytes):
        n = params[0]

        img = Image.open(io.BytesIO(data))
        print("image opened")

        width, height = img.size
        tile_width_base = width // n
        tile_height_base = height // n

        tiles = []

        # split image in n^2 tiles
        for i in range(n):
            for j in range(n):
                left = j * tile_width_base
                upper = i * tile_height_base
                right = (j + 1) * tile_width_base if j < n - 1 else width
                lower = (i + 1) * tile_height_base if i < n - 1 else height

                tile = img.crop((left, upper, right, lower))

                tile_bytes_io = io.BytesIO()
                tile.save(tile_bytes_io, format='PNG')
                tile_bytes = tile_bytes_io.getvalue()

                tiles.append(tile_bytes)

        # Restituisce i tiles come lista di oggetti bytes
        return tiles




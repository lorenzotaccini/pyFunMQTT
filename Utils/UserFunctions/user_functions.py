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


# input: list of dict, output: dict{outtopic: payload}
class ExtractCols(Service):
    def serve(self, params: dict, data: list) -> dict:
        res = {}
        for elem in data:  # for every row (a row is a dict)
            for k, v in elem.items():  # for every column
                if k in params['parameters']:
                    if k not in res.keys():
                        res[k] = []
                    res[k].append(v)
        return res


class SplitTable(Service):
    def serve(self, params: dict, data: list) -> Any:
        # Estrai tutte le chiavi (colonne) dalla prima riga
        keys = list(table[0].keys())

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
            for row in table:
                sub_table_row = {key: row[key] for key in current_keys}
                sub_tables[i].append(sub_table_row)

            # Aggiorna l'indice di partenza per la prossima iterazione
            start_index = end_index

        return sub_tables


class ImageSplit(Service):

    def serve(self, params, data: Image):
        n = params[0]

        # Decodifica la stringa in bytes
        data_bytes = bytearray(data)

        # Ora puoi aprire l'immagine
        img = Image.open(io.BytesIO(data_bytes))

        print(type(data))

        print("image opened")

        # Dimensioni dell'immagine
        width, height = img.size

        # Calcola le dimensioni dei tiles: la divisione esatta più l'eventuale resto
        tile_width_base = width // n
        tile_height_base = height // n

        # Lista per memorizzare i tiles come oggetti bytes
        tiles = []

        # Dividi l'immagine in n^2 tiles
        for i in range(n):
            for j in range(n):
                # Calcola le dimensioni dei bordi per ciascun tile
                left = j * tile_width_base
                upper = i * tile_height_base
                # Se è l'ultima colonna, includi il resto della larghezza
                right = (j + 1) * tile_width_base if j < n - 1 else width
                # Se è l'ultima riga, includi il resto dell'altezza
                lower = (i + 1) * tile_height_base if i < n - 1 else height

                # Crea il tile corrente
                tile = img.crop((left, upper, right, lower))

                # Converti il tile in un oggetto bytes
                tile_bytes_io = io.BytesIO()
                tile.save(tile_bytes_io, format='PNG')
                tile_bytes = tile_bytes_io.getvalue()

                # Aggiungi il tile alla lista
                tiles.append(tile_bytes)

        # Restituisce i tiles come lista di oggetti bytes
        return tiles

class Upper(Service):
    def serve(self, params, data: str):
        return str(data).upper()


class Extract(Service):
    def serve(self, params, data: Any):
        pass


def split_table_by_columns(table, n):
    """
    Divide una tabella (lista di dizionari) in n parti, suddividendo le colonne.

    Args:
    - table (list of dict): La tabella originale da dividere.
    - n (int): Il numero di parti in cui dividere la tabella.

    Returns:
    - list of list of dict: Una lista contenente n tabelle suddivise per colonne.
    """
    if not table:
        return [[] for _ in range(n)]

    # Estrai tutte le chiavi (colonne) dalla prima riga
    keys = list(table[0].keys())

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
        for row in table:
            sub_table_row = {key: row[key] for key in current_keys}
            sub_tables[i].append(sub_table_row)

        # Aggiorna l'indice di partenza per la prossima iterazione
        start_index = end_index

    return sub_tables


if __name__ == '__main__':
    # Esempio di utilizzo
    table = [
        {'id': 1, 'name': 'Alice', 'age': 30, 'city': 'New York', 'cc': 'ciao'},
        {'id': 2, 'name': 'Bob', 'age': 25, 'city': 'Los Angeles', 'cc': 'come'},
        {'id': 3, 'name': 'Charlie', 'age': 35, 'city': 'Chicago', 'cc': 'va'},
    ]

    n = 3
    sub_tables = split_table_by_columns(table, n)
    for i, sub_table in enumerate(sub_tables):
        print(f"Subtable {i + 1}: {sub_table}")

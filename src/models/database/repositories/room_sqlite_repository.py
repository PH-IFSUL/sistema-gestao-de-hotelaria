import sqlite3
from typing import List, Optional
from models.room.room import Room
from models.room import state_room as st

ESTADOS = {
    "disponivel": st.Available,
    "reservado":  st.Reserved,
    "ocupado":    st.Ocupied,
    "limpeza":    st.Cleaning,
    "manutencao": st.Maintenance,
}


class SQLite_Room_Repository:

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conn = conexao

    @staticmethod
    def _to_room(row: sqlite3.Row) -> Room:
        quarto = Room(row["numero"], row["tipo"], row["valor_diaria"])
        quarto.estado.set_estado(ESTADOS[row["estado"]]())
        return quarto

    def add(self, quarto: Room) -> None:
        try:
            with self._conn:
                self._conn.execute(
                    "INSERT INTO room (numero, tipo, valor_diaria, estado) "
                    "VALUES (?, ?, ?, ?)",
                    (quarto.get_numero(), quarto.get_tipo(),
                     quarto.get_valor_diaria(), str(quarto.estado)))
        except sqlite3.IntegrityError:
            raise ValueError(f"Já existe um quarto com o"
                             f" número {quarto.get_numero()}.")

    def list(self) -> List[Room]:
        rows = self._conn.execute(
            "SELECT * FROM room ORDER BY numero").fetchall()
        return [self._to_room(r) for r in rows]

    def find_by_number(self, number_query: int) -> Optional[Room]:
        row = self._conn.execute(
            "SELECT * FROM room WHERE numero = ?", (number_query,)).fetchone()
        return self._to_room(row) if row else None

    def delete(self, number_query: int) -> bool:
        try:
            with self._conn:
                cur = self._conn.execute(
                    "DELETE FROM room WHERE numero = ?", (number_query,))
        except sqlite3.IntegrityError:
            raise ValueError("Quarto possui estadias registradas e não "
                             "pode ser removido.")
        return cur.rowcount > 0

    def get_types(self) -> List[str]:
        rows = self._conn.execute(
            "SELECT DISTINCT tipo FROM room ORDER BY tipo").fetchall()
        return [r["tipo"] for r in rows]

    def update(self, quarto: Room) -> bool:
        with self._conn:
            cur = self._conn.execute(
                "UPDATE room SET tipo = ?, valor_diaria = ?, estado = ? "
                "WHERE numero = ?",
                (quarto.get_tipo(), quarto.get_valor_diaria(),
                 str(quarto.estado), quarto.get_numero()))
        return cur.rowcount > 0
import sqlite3
from datetime import date, datetime
from typing import Optional
from models.room.room import Room
from models.client.client import Client
from models.client.stay_info import Guest_Stay
from models.invoice.invoice import Guest_Bill
from models.invoice.itens import Bill_Item, Item
from models.database.repositories.client_sqlite_repository import SQLite_Client_Repository
from models.database.repositories.room_sqlite_repository import SQLite_Room_Repository


class SQLite_Stay_Repository:

    def __init__(self,
                 conexao: sqlite3.Connection,
                 client_repo: SQLite_Client_Repository,
                 room_repo: SQLite_Room_Repository) -> None:
        self._conn = conexao
        self._client_repo = client_repo
        self._room_repo = room_repo

    def _to_stay(self, row: sqlite3.Row) -> Guest_Stay:
        cliente = self._client_repo.find_by_id(row["client_id"])
        quarto = (self._room_repo.find_by_number(row["room_numero"])
                  if row["room_numero"] is not None else None)
        estadia = Guest_Stay(cliente, quarto,
                             datetime.fromisoformat(row["checkin"]),
                             datetime.fromisoformat(row["checkout"]))
        estadia.id = row["id"]
        bill = self.get_bill(row["id"])
        if bill:
            estadia.guest_bill = bill
        return estadia

    def get_next_id(self) -> int:
        row = self._conn.execute(
            "SELECT seq FROM sqlite_sequence WHERE name = 'stay'").fetchone()
        return (row["seq"] if row else 0) + 1

    def save(self, estadia: Guest_Stay) -> None:
       
        if estadia.guest.get_id() is None:
            raise ValueError("O cliente precisa estar cadastrado antes de "
                             "criar a estadia.")
        numero = (estadia.room_number.get_numero()
                  if estadia.room_number else None)
        dados = (estadia.guest.get_id(), numero,
                 estadia.checkin_date.isoformat(),
                 estadia.checkout_date.isoformat())
        try:
            with self._conn:
                if estadia.id is None:
                    cur = self._conn.execute(
                        "INSERT INTO stay (client_id, room_numero, checkin, "
                        "checkout) VALUES (?, ?, ?, ?)", dados)
                    estadia.id = cur.lastrowid
                else:
                    self._conn.execute(
                        "UPDATE stay SET client_id = ?, room_numero = ?, "
                        "checkin = ?, checkout = ? WHERE id = ?",
                        dados + (estadia.id,))
                    self._conn.execute(
                        "DELETE FROM bill_item WHERE stay_id = ?",
                        (estadia.id,))
                estadia.guest_bill.id_stay = estadia.id
                for bi in estadia.guest_bill.itens:
                    self._insert_bill_item(estadia.id, bi)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Dados inválidos para a estadia: {e}")

    def delete(self, stay_id: int) -> bool:
        with self._conn:
            cur = self._conn.execute(
                "DELETE FROM stay WHERE id = ?", (stay_id,))
        return cur.rowcount > 0

    def get_bill(self, id_stay: int) -> Optional[Guest_Bill]:
        if not self._conn.execute("SELECT 1 FROM stay WHERE id = ?",
                                  (id_stay,)).fetchone():
            return None
        bill = Guest_Bill(id_stay)
        rows = self._conn.execute(
            "SELECT b.id AS bid, b.quantidade, b.preco_unitario, "
            "       i.id AS iid, i.nome "
            "FROM bill_item b JOIN item i ON i.id = b.item_id "
            "WHERE b.stay_id = ? ORDER BY b.id", (id_stay,)).fetchall()
        for r in rows:
            item = Item(r["iid"], r["nome"], float(r["preco_unitario"]))
            bill.add_itens(Bill_Item(r["bid"], item, r["quantidade"]))
        return bill

    def add_itens_to_bill(self, id_stay: int, item: Bill_Item) -> None:
        if not self._conn.execute("SELECT 1 FROM stay WHERE id = ?",
                                  (id_stay,)).fetchone():
            raise ValueError(f"Estadia {id_stay} não encontrada.")
        with self._conn:
            self._insert_bill_item(id_stay, item)

    def _insert_bill_item(self, id_stay: int, bi: Bill_Item) -> None:
       
        self._conn.execute(
            "INSERT OR IGNORE INTO item (id, nome, preco) VALUES (?, ?, ?)",
            (bi.item.id, bi.item.name, bi.item.price))
        cur = self._conn.execute(
            "INSERT INTO bill_item (stay_id, item_id, quantidade, "
            "preco_unitario) VALUES (?, ?, ?, ?)",
            (id_stay, bi.item.id, bi.quantity, bi.item.price))
        bi.id = cur.lastrowid

    def find_by_id(self, id_query: int) -> Optional[Guest_Stay]:
        row = self._conn.execute(
            "SELECT * FROM stay WHERE id = ?", (id_query,)).fetchone()
        return self._to_stay(row) if row else None

    def find_by_cpf(self, cpf_query: str) -> Optional[Guest_Stay]:
        
        row = self._conn.execute(
            "SELECT s.* FROM stay s JOIN client c ON c.id = s.client_id "
            "WHERE c.cpf = ? ORDER BY s.checkin DESC, s.id DESC LIMIT 1",
            (cpf_query,)).fetchone()
        return self._to_stay(row) if row else None

    def get_date_reservations(self, date: date) -> list[Guest_Stay]:
        
        d = date.isoformat()
        rows = self._conn.execute(
            "SELECT * FROM stay WHERE date(checkin) <= ? AND ? < date(checkout) "
            "AND status != 'CANCELADA' ORDER BY checkin", (d, d)).fetchall()
        return [self._to_stay(r) for r in rows]

    def update_room(self, id_stay: int, room: Room) -> bool:
        with self._conn:
            cur = self._conn.execute(
                "UPDATE stay SET room_numero = ? WHERE id = ?",
                (room.get_numero(), id_stay))
        return cur.rowcount > 0

    def update_client(self, id_stay: int, client: Client) -> bool:
        with self._conn:
            cur = self._conn.execute(
                "UPDATE stay SET client_id = ? WHERE id = ?",
                (client.get_id(), id_stay))
        return cur.rowcount > 0

    def room_has_conflict(self, room_numero: int,
                          checkin: datetime, checkout: datetime,
                          ignore_stay_id: int | None = None) -> bool:
        
        row = self._conn.execute(
            "SELECT 1 FROM stay WHERE room_numero = ? AND status != 'CANCELADA' "
            "AND checkin < ? AND checkout > ? AND id != ? LIMIT 1",
            (room_numero, checkout.isoformat(), checkin.isoformat(),
             ignore_stay_id if ignore_stay_id is not None else -1)).fetchone()
        return row is not None
"""python -m unittest discover -s tests -v"""
import sqlite3
import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models.database.connection import Database_Connection
from models.database.repositories.client_sqlite_repository import SQLite_Client_Repository
from models.database.repositories.room_sqlite_repository import SQLite_Room_Repository
from models.database.repositories.stay_sqlite_repository import SQLite_Stay_Repository
from models.client.client import Client
from models.client.stay_info import Guest_Stay
from models.room.room import Room
from models.room.state_room import Maintenance
from models.invoice.itens import Item, Bill_Item


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.db = Database_Connection(":memory:")
        self.conn = self.db.get_connection()
        self.clients = SQLite_Client_Repository(self.conn)
        self.rooms = SQLite_Room_Repository(self.conn)
        self.stays = SQLite_Stay_Repository(self.conn, self.clients, self.rooms)

    def tearDown(self):
        self.db.close()

    def novo_cliente(self, cpf="12345678901"):
        c = Client("Maria", cpf, "5499999", "m@x.com")
        self.clients.save(c)
        return c


class TestClient(BaseTest):
    def test_save_gera_id_e_busca(self):
        c = self.novo_cliente()
        self.assertEqual(c.get_id(), 1)
        self.assertEqual(self.clients.find_by_Cpf("12345678901").get_nome(), "Maria")
        self.assertEqual(self.clients.find_by_id(1).get_cpf(), "12345678901")
        self.assertIsNone(self.clients.find_by_id(99))

    def test_cpf_duplicado(self):
        self.novo_cliente()
        with self.assertRaises(ValueError):
            self.novo_cliente()

    def test_update_delete_list(self):
        c = self.novo_cliente()
        self.novo_cliente("98765432100")
        c._nome = "Maria Silva"
        self.assertTrue(self.clients.update(c))
        self.assertEqual(self.clients.find_by_id(c.get_id()).get_nome(), "Maria Silva")
        self.assertEqual(len(self.clients.get_all()), 2)
        self.assertTrue(self.clients.delete("12345678901"))
        self.assertFalse(self.clients.delete("12345678901"))
        self.assertEqual(len(self.clients.get_all()), 1)


class TestRoom(BaseTest):
    def test_add_list_duplicado(self):
        self.rooms.add(Room(101, "Simples", 100.0))
        self.rooms.add(Room(102, "Suíte", 300.0))
        with self.assertRaises(ValueError):
            self.rooms.add(Room(101, "Duplo", 200.0))
        self.assertEqual([q.get_numero() for q in self.rooms.list()], [101, 102])
        self.assertEqual(self.rooms.get_types(), ["Simples", "Suíte"])

    def test_estado_persiste(self):
        q = Room(101, "Simples", 100.0)
        self.rooms.add(q)
        q.estado.start_maintenance(q)
        self.assertTrue(self.rooms.update(q))
        carregado = self.rooms.find_by_number(101)
        self.assertIsInstance(carregado.estado._state, Maintenance)
        self.assertEqual(carregado.estado.get_current(), "Em Manutenção")

    def test_todos_estados_mapeados(self):
        from models.database.repositories.room_sqlite_repository import ESTADOS
        for tag, cls in ESTADOS.items():
            self.assertEqual(str(cls()), tag)

    def test_delete(self):
        self.rooms.add(Room(101, "Simples", 100.0))
        self.assertTrue(self.rooms.delete(101))
        self.assertFalse(self.rooms.delete(101))


class TestStay(BaseTest):
    def setUp(self):
        super().setUp()
        self.c = self.novo_cliente()
        self.q = Room(101, "Duplo", 200.0)
        self.rooms.add(self.q)
        self.ent = datetime(2026, 12, 1, 14)
        self.sai = datetime(2026, 12, 4, 12)

    def criar(self):
        s = Guest_Stay(self.c, self.q, self.ent, self.sai)
        self.stays.save(s)
        return s

    def test_save_e_find(self):
        s = self.criar()
        self.assertEqual(s.id, 1)
        achada = self.stays.find_by_id(1)
        self.assertEqual(achada.guest.get_cpf(), self.c.get_cpf())
        self.assertEqual(achada.room_number.get_numero(), 101)
        self.assertEqual(achada.checkin_date, self.ent)
        self.assertEqual(self.stays.find_by_cpf(self.c.get_cpf()).id, 1)
        self.assertEqual(self.stays.get_next_id(), 2)

    def test_fatura(self):
        s = self.criar()
        agua = Item(10, "Água", 5.0)
        self.stays.add_itens_to_bill(s.id, Bill_Item(0, agua, 3))
        self.stays.add_itens_to_bill(s.id, Bill_Item(0, Item(1, "Frigobar", 15.0), 1))
        bill = self.stays.get_bill(s.id)
        self.assertEqual(len(bill.itens), 2)
        self.assertAlmostEqual(bill.calculate_total(), 30.0)
        self.assertAlmostEqual(self.stays.find_by_id(s.id).get_total(), 30.0)
        self.assertIsNone(self.stays.get_bill(999))

    def test_save_com_itens_no_objeto(self):
        s = Guest_Stay(self.c, self.q, self.ent, self.sai)
        s.add_item(Bill_Item(0, Item(1, "Frigobar", 15.0), 2))
        self.stays.save(s)
        self.assertAlmostEqual(self.stays.find_by_id(s.id).get_total(), 30.0)

    def test_datas_e_conflito(self):
        self.criar()
        self.assertEqual(len(self.stays.get_date_reservations(date(2026, 12, 2))), 1)
        self.assertEqual(len(self.stays.get_date_reservations(date(2026, 12, 4))), 0)
        self.assertTrue(self.stays.room_has_conflict(
            101, datetime(2026, 12, 3), datetime(2026, 12, 6)))
        self.assertFalse(self.stays.room_has_conflict(
            101, self.sai, datetime(2026, 12, 6)))

    def test_checkout_invalido(self):
        with self.assertRaises(ValueError):
            self.stays.save(Guest_Stay(self.c, self.q, self.sai, self.ent))

    def test_integridade_referencial(self):
        self.criar()
        with self.assertRaises(ValueError):
            self.clients.delete(self.c.get_cpf())
        with self.assertRaises(ValueError):
            self.rooms.delete(101)
        self.assertTrue(self.stays.delete(1))
        self.assertTrue(self.rooms.delete(101))

    def test_update_room_client(self):
        s = self.criar()
        outro = Room(102, "Suíte", 300.0)
        self.rooms.add(outro)
        self.assertTrue(self.stays.update_room(s.id, outro))
        self.assertEqual(self.stays.find_by_id(s.id).room_number.get_numero(), 102)
        c2 = self.novo_cliente("98765432100")
        self.assertTrue(self.stays.update_client(s.id, c2))
        self.assertEqual(self.stays.find_by_id(s.id).guest.get_cpf(), "98765432100")

    def test_cascade_fatura(self):
        s = self.criar()
        self.stays.add_itens_to_bill(s.id, Bill_Item(0, Item(1, "Frigobar", 15.0), 1))
        self.stays.delete(s.id)
        n = self.conn.execute("SELECT COUNT(*) FROM bill_item").fetchone()[0]
        self.assertEqual(n, 0)


class TestPersistenciaArquivo(unittest.TestCase):
    def test_dados_sobrevivem_reabrir(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            caminho = Path(d) / "sub" / "hotel.db"
            db = Database_Connection(caminho)
            SQLite_Client_Repository(db.get_connection()).save(
                Client("Ana", "11122233344", "123", ""))
            db.close()
            db = Database_Connection(caminho)  
            self.assertEqual(
                len(SQLite_Client_Repository(db.get_connection()).get_all()), 1)
            db.close()


if __name__ == "__main__":
    unittest.main()
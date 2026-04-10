import sqlite3
from config import EQUIPMENT_DB_PATH


def create_database():
    conn = sqlite3.connect(EQUIPMENT_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id TEXT PRIMARY KEY,
            name TEXT,
            location TEXT,
            installed_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id TEXT,
            date TEXT,
            event_type TEXT,
            description TEXT,
            technician TEXT,
            UNIQUE(equipment_id, date, event_type)
        )
    """)

    equipment_list = [
        ("PUMP-001", "Centrifugal Pump", "Factory Floor A", "2020-03-15"),
        ("MOTOR-047", "AC Induction Motor", "Production Line B", "2019-07-22"),
        ("CONVEYOR-003", "Belt Conveyor", "Warehouse Section C", "2021-01-10"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO equipment VALUES (?, ?, ?, ?)
    """, equipment_list)

    history_list = [
        ("PUMP-001", "2023-01-10", "routine_service", "Oil changed, seals inspected", "John Smith"),
        ("PUMP-001", "2023-06-22", "repair", "Bearing replaced due to noise", "Maria Lopez"),
        ("PUMP-001", "2024-02-14", "routine_service", "Full inspection passed", "John Smith"),
        ("PUMP-001", "2024-09-01", "alert", "Temperature spike recorded by sensor", "System"),
        ("MOTOR-047", "2023-03-05", "repair", "Winding repaired after overload", "Ahmed Khan"),
        ("MOTOR-047", "2024-01-18", "routine_service", "Lubrication and alignment check", "Maria Lopez"),
        ("CONVEYOR-003", "2023-11-30", "repair", "Belt replaced after tear", "John Smith"),
        ("CONVEYOR-003", "2024-05-20", "routine_service", "Rollers cleaned and tensioned", "Ahmed Khan"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO maintenance_history 
        (equipment_id, date, event_type, description, technician)
        VALUES (?, ?, ?, ?, ?)
    """, history_list)

    conn.commit()
    conn.close()


def get_equipment_history(equipment_id: str) -> list:
    create_database()

    conn = sqlite3.connect(EQUIPMENT_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, event_type, description, technician
        FROM maintenance_history
        WHERE equipment_id = ?
        ORDER BY date DESC
    """, (equipment_id,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return [{"date": "N/A", "event_type": "none", "description": f"No history found for {equipment_id}", "technician": "N/A"}]

    return [
        {
            "date": row[0],
            "event_type": row[1],
            "description": row[2],
            "technician": row[3]
        }
        for row in rows
    ]
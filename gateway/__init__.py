"""Gateway Package."""

import base64
import json
import time
from typing import NoReturn

import click
import hexdump
import psycopg2
import serial
from rich.console import Console
from rich.json import JSON

console = Console()


def connect_to_database(dbname: str, host: str, user: str, password: str, port: str):
    conn: psycopg2.Connection
    is_connected: bool = False

    while not is_connected:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                host=host,
                user=user,
                password=password,
                port=port,
            )
            is_connected = True
        except Exception as e:
            console.log(f"[ERROR] {e}")
            time.sleep(2)

    return conn


@click.command()
@click.option("--device", "-D", default="/dev/ttyUSB0")
@click.option("--dbname", "-d", default="h10")
@click.option("--host", "-h", default="localhost")
@click.option("--user", "-u", prompt=True)
@click.password_option()
@click.option("--port", "-p", default="5432")
def cli(
    device: str,
    host: str,
    user: str,
    password: str,
    port: str,
    dbname: str,
) -> NoReturn:
    """CLI for the Gateway.

    Args:
    ----
        device (str): device
        host (str): host name (localhost)
        user (str): PostgreSQL User
        password (str): PostgreSQL Password
        port (str): PostgreSQL Port
        dbname (str): PostgreSQL database name

    Returns:
    -------
        NoReturn: _description_
    """
    ser = serial.Serial(device, 115200)
    ser.timeout = None

    conn = connect_to_database(
        dbname=dbname,
        host=host,
        user=user,
        password=password,
        port=port,
    )

    while True:
        data_raw = ser.readline()

        if data_raw:
            try:
                console.log("-" * 100)
                data = data_raw.decode("ascii", errors="ignore")

                data_json: dict[str, str] = json.loads(data)
                rssi: str | None = data_json.get("rssi")
                snr: str | None = data_json.get("snr")

                b64_data = base64.b64decode(data_json.get("payload"))

                payload: dict = json.loads(b64_data)

                data_json["payload"] = payload

                console.log("[DATA]", JSON(json.dumps(data_json)))
            except Exception as e:
                console.log(e)
                console.log(hexdump.hexdump(data_raw))
                continue

            curr = conn.cursor()

            curr.execute(
                "INSERT INTO h10_logs (cpu_id, rssi, snr, temp, hum, vcc, vpanel)\n"
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                [
                    payload.get("cpuid"),
                    rssi,
                    snr,
                    payload.get("temp"),
                    payload.get("hum"),
                    payload.get("vcc"),
                    payload.get("vpanel"),
                ],
            )

            conn.commit()


if __name__ == "__main__":
    cli()

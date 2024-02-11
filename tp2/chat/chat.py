import asyncio
import logging

log_file_path = 'www/server.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')

CLIENTS = {}
ROOMS = {}

async def broadcast_message(room, message, exclude_writer=None):
    for client in ROOMS[room].values():
        if client["w"] is not exclude_writer:
            try:
                client["w"].write(message.encode())
                await client["w"].drain()
            except ConnectionError:
                pass

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    first_data = await reader.read(1024)
    pseudo, room = first_data.decode().split("|")[1:3] if first_data.startswith(b"Hello|") else ("Inconnu", "default")

    if room not in ROOMS:
        ROOMS[room] = {}
    CLIENTS[addr] = {"r": reader, "w": writer, "pseudo": pseudo, "room": room}
    ROOMS[room][addr] = CLIENTS[addr]

    logging.info(f"Client {pseudo} connecté à {room} : {addr}")
    await broadcast_message(room, f"Annonce : {pseudo} a rejoint la room {room}")

    while True:
        data = await reader.read(1024)
        if not data:
            del ROOMS[room][addr]
            if not ROOMS[room]:
                del ROOMS[room]
            logging.info(f"Client {pseudo} a quitté la room {room}")
            break
        message = f"{CLIENTS[addr]['pseudo']} a dit : {data.decode()}"
        await broadcast_message(room, message, exclude_writer=writer)

    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 5000)
    addr = server.sockets[0].getsockname()
    logging.info(f"Serveur démarré sur {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
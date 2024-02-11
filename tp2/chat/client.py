import asyncio
import aioconsole
import logging

log_file_path = 'www/client.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')

async def send_message(writer):
    while True:
        message = await aioconsole.ainput("Message: ")
        writer.write(message.encode())
        await writer.drain()
        logging.info(f"Message envoyé : {message}")

async def receive_message(reader):
    while True:
        data = await reader.read(1024)
        if not data:
            print("Le serveur s'est déconnecté.")
            logging.info("Déconnecté du serveur.")
            break
        message = data.decode()
        print(f"Reçu: {message}")
        logging.info(f"Message reçu : {message}")

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 5000)

    pseudo = input("Entrez votre pseudo: ")
    room = input("Entrez le nom de la room: ")
    writer.write(f"Hello|{pseudo}|{room}".encode())

    send_task = asyncio.create_task(send_message(writer))
    receive_task = asyncio.create_task(receive_message(reader))

    await asyncio.gather(send_task, receive_task)

if __name__ == '__main__':
    asyncio.run(main())
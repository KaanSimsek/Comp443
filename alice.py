from DiffieHellman import DiffieHellman
import time
from Messager import Messager
import asyncio


file_name = "Communication.txt" # For part 4 change to alice.txt


alice = DiffieHellman("Alice", file_name)
alice.publishKey()

key = alice.readKey()

alice.genKey(key)


messager = Messager("Alice", file_name, alice.key)


print('Enter message:')
message = input()
messager.send_message(message)


async def whatsapp():
    while True:
        try:
            output = await messager.read_message()  # Await the message asynchronously
            print(output)
        except asyncio.CancelledError:
            break  # Handle cancellation gracefully

        print('Enter message:')
        message = input()
        messager.send_message(message)

asyncio.run(whatsapp())
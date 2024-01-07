from DiffieHellman import DiffieHellman
import time
from Messager import Messager
import asyncio



file_name = "Communication.txt" # For part 4 change to bob.txt

bob =  DiffieHellman("Bob", file_name)
bob.publishKey()

key = bob.readKey()

bob.genKey(key)
print("shared secret:",bob.key)


messager = Messager("Bob", file_name, bob.key)


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
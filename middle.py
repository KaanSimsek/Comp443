from AttackerDiffieHellman import AttackerDiffieHellman
import time
from AttackerMessager import AttackerMessager
import asyncio


alice_file = "alice.txt"
bob_file = "bob.txt"

attacker = AttackerDiffieHellman(alice_file, bob_file)

attacker.publishKey()
alice_key = attacker.readAliceKey()
bob_key = attacker.readBobKey()

attacker.genKey(alice_key)
alice_secret = attacker.key
attacker.genKey(bob_key)
bob_secret = attacker.key


attackerMessager=AttackerMessager(alice_file, bob_file, alice_secret, bob_secret)

async def whatsapp():
    iteration=0
    while True:
        try:
            if iteration%2==0:
                output = await attackerMessager.read_alice_message()
            else:
                output = await attackerMessager.read_bob_message()

            print(output)
        except asyncio.CancelledError:
            break  # Handle cancellation gracefully

        print('Change message:')
        message = input()
        if iteration%2==0:
            attackerMessager.send_message_to_bob(message)
        else:
            attackerMessager.send_message_to_alice(message)
        iteration+=1

asyncio.run(whatsapp()) 




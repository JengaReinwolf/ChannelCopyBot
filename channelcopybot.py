import argparse
import asyncio
import json
import time

import discord

parser = argparse.ArgumentParser()
parser.add_argument("from_channel", type=int)
parser.add_argument("to_channel", type=int)
parser.add_argument("--delay", type=int)
parser.add_argument("--start_at", type=int)
args = parser.parse_args()

client = discord.Client()
with open("config.json", "rb") as f:
    config = json.loads(f.read())

async def copy():
    await client.wait_until_ready()

    to_channel = client.get_channel(args.to_channel)
    from_channel = client.get_channel(args.from_channel)

    after_message = None
    if args.start_at:
        after_message = await from_channel.fetch_message(args.start_at)

    counter = 0
    async for message in from_channel.history(limit=10000, oldest_first=True, after=after_message):
        counter += 1
        if not message.content and not message.attachments:
            continue  # Skip empty message
        if message.attachments:
            await to_channel.send(message.content, files=[await a.to_file() for a in message.attachments])
        else:
            await to_channel.send(message.content)
        if args.delay:
            time.sleep(args.delay)
    print("Copied {} messages".format(counter))

client.loop.create_task(copy())
client.run(config["token"])

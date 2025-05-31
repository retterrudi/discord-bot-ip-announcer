import os
import requests
import discord
import asyncio
from dotenv import load_dotenv


def get_my_ip() -> str:
    response = requests.get("https://api.ipify.org", timeout=5)
    if response.status_code != 200:
        raise(Exception(f"An error occurred during ip fetching: \n\tStatus code: {response.status_code}\n\tResponse: {response.content}"))

    return response.text


async def main():
    intents = discord.Intents.default()
    intents.guilds = True

    client = discord.Client(intents=intents)

    load_dotenv(".env")
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    target_channel_id = int(os.getenv("TARGET_CHANNEL_ID"))

    @client.event
    async def on_ready():
        print(f'{client.user.name} has connected to Discord!')
        print(f'Bot ID: {client.user.id}')

        print(list(filter(lambda item: 'bot' in str(item), client.get_all_channels())))
        target_channel = client.get_channel(target_channel_id)


        if not target_channel:
            print(f'Error: Target channel with ID `{target_channel_id}` not found.')
            print('Make sure the bot is in the server and the channel ID is correct.')
            await client.close()
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blurple()
        )

        embed.add_field(name="Server-IP", value=server_ip, inline=False)

        embed.set_footer(text=footer)

        try:
            await target_channel.send(embed=embed)
            print(f'Formatted message sent to channel: {target_channel.name} ({target_channel.id})')
        except discord.Forbidden:
            print(f'Error: I don\'t have permission to send messages in {target_channel.mention}.')
        except Exception as e:
            print(f'An unexpected error occurred while sending the message: {e}')
        finally:
            print('Closing connection')
            await client.close()
            print('Connection closed. Script finished.')



    title = "IP-Announcement"
    description = "The minecraft server has been started."
    server_ip = get_my_ip()
    server_ip += ":6764"

    footer = "Automated Message"


    try: 
        await client.start(bot_token)
    except discord.LoginFailure: 
        print('Error: Failed to log in. Check your bot token.')
    except Exception as e: 
        print(f'An error occurred during bot operation: {e}')
    finally:
        if not client.is_closed():
            await client.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt: 
        print("Script interrupted by user. Closing connection if open")

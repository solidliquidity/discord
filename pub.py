import asyncio
import nats
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration - Replace with your actual values
NATS_SERVER = "nats://localhost:4222"  # NATS server URL

async def publish_command(command):
    try:
        # Connect to NATS server
        nc = await nats.connect(getenv('NATS_SERVER', NATS_SERVER))
        
        # Publish the command
        await nc.publish(f"discord.command.{command}", b'')
        
        # Close the connection
        await nc.drain()
        
        print(f"Command '{command}' published to NATS")
    except Exception as e:
        print(f"Error publishing command: {e}")

# Example usage
async def main():
    # Choose which command to run
    command = input("Enter command to send (report/hello): ").strip().lower()
    
    if command in ["report", "hello"]:
        await publish_command(command)
    else:
        print("Invalid command. Please use 'report' or 'hello'.")
    
    # You could also schedule commands
    # Example of scheduled reporting:
    """
    while True:
        # Send report every hour
        await publish_command("report")
        print("Scheduled report sent. Waiting for 1 hour...")
        await asyncio.sleep(3600)  # Wait 1 hour
    """

if __name__ == "__main__":
    asyncio.run(main())
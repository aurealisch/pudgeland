import os

import dotenv

dotenv.load_dotenv()

gateway_bot_token = os.getenv("GATEWAY_BOT_TOKEN")

java_server_host = os.getenv("JAVA_SERVER_HOST")
java_server_port = int(os.getenv("JAVA_SERVER_PORT"))

private_voice_channel_guild_id = int(os.getenv("PRIVATE_VOICE_CHANNEL_GUILD_ID"))
private_voice_channel_category_id = int(os.getenv("PRIVATE_VOICE_CHANNEL_CATEGORY_ID"))

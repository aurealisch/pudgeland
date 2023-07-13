import os

import dotenv

dotenv.load_dotenv()

gateway_bot_token = os.getenv("GATEWAY_BOT_TOKEN")

java_server_host = os.getenv("JAVA_SERVER_HOST")
java_server_port = int(os.getenv("JAVA_SERVER_PORT"))

database_url = os.getenv("DATABASE_URL")

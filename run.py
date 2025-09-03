from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app(config_mode=os.getenv('CONFIG_MODE'))

if __name__ == '__main__':
	app.run(
	host='0.0.0.0',
	port=os.getenv('PORT') or 8080,
)
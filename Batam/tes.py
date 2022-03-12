from dotenv import load_dotenv
import os
# Env variable
load_dotenv()


print(os.getenv('MQTT_USERNAME'))
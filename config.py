from dotenv import load_dotenv
import os

load_dotenv('.env')

NAME_CRAWLER='vea'

CHROMEDRIVER_PATH='/home/michael/Documents/projects/chromedriver-v-146.0.7680/chromedriver'

EMAIL=os.environ.get('EMAIL')
PASSWORD=os.environ.get('PASSWORD')




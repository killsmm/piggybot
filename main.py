from piggyBot import PiggyBot
from dotenv import load_dotenv
import os


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('BOT_TOKEN')
    PREFIX = os.getenv('BOT_PREFIX', '.')
    YTDL_FORMAT = os.getenv('YTDL_FORMAT', 'worstaudio')
    PRINT_STACK_TRACE = os.getenv('PRINT_STACK_TRACE', '1').lower() in ('true', 't', '1')
    BOT_REPORT_COMMAND_NOT_FOUND = os.getenv('BOT_REPORT_COMMAND_NOT_FOUND', '1').lower() in ('true', 't', '1')
    BOT_REPORT_DL_ERROR = os.getenv('BOT_REPORT_DL_ERROR', '0').lower() in ('true', 't', '1')

    bot = PiggyBot.get_instance()
    bot.run(TOKEN)
import asyncio
import html
import json
import logging
import traceback
from datetime import datetime

import pytz
from dotenv import load_dotenv, find_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, Application, AIORateLimiter

from utils import get_env, get_chat_ids, ENV, is_token_expired, renew_api_token, get_rates, report_health

load_dotenv(dotenv_path=find_dotenv())

logging.basicConfig(
    format=get_env(ENV.LOG_FORMAT),
    level=get_env(ENV.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

chat_ids = get_chat_ids()


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised\n"
        f"update = {json.dumps(update_str, indent=2, ensure_ascii=False)}\n"
        f"context.chat_data = {str(context.chat_data)}\n"
        f"context.user_data = {str(context.user_data)}\n"
        f"{tb_string}"
    )
    logger.error(message)


async def health_check(context: ContextTypes.DEFAULT_TYPE):
    report_health(get_env(ENV.HEALTH_CHECK_PUSH_URL))


async def report_exchange_rates(context: ContextTypes.DEFAULT_TYPE):
    api_token = get_env(ENV.API_TOKEN)
    if is_token_expired(api_token):
        logger.info(f'Renew API token. Existing API token - {api_token}')
        api_token = renew_api_token()
    r = get_rates(get_env(ENV.API_HOST), api_token, get_env(ENV.SYMBOLS))
    logger.info(f'Response from API server {r}')
    try:
        r['json']['timestamp'] = datetime.strptime(r['json']['timestamp'], get_env(ENV.JSON_TIMESTAMP_FORMAT)) \
            .astimezone(pytz.UTC).astimezone(pytz.timezone(get_env(ENV.DISPLAY_TZ)))
    except:
        logger.error(f'Unable to convert timestamp string {r["json"]["timestamp"]} using format {get_env(ENV.JSON_TIMESTAMP_FORMAT)}')
    message = [f'{_["symbol"]}: {_["rate"]}' for _ in r['json']['rates']]
    message.append(f'({r["json"]["timestamp"].strftime(get_env(ENV.DISPLAY_TIMESTAMP_FORMAT)) if isinstance(r["json"]["timestamp"], datetime) else r["json"]["timestamp"]})')
    for user_id in chat_ids['users']:
        await context.bot.send_message(chat_id=user_id, text='\r\n'.join(message))


if __name__ == '__main__':
    application = Application.builder().token(get_env(ENV.TELEGRAM_BOT_TOKEN)).rate_limiter(AIORateLimiter()).build()

    first = datetime.now().replace(minute=int(get_env(ENV.FIRST_MINUTE)), second=0, microsecond=0).astimezone(pytz.UTC)
    application.job_queue.run_repeating(report_exchange_rates, interval=int(get_env(ENV.REPORT_FREQUENCY)), first=first)
    application.job_queue.run_repeating(health_check, interval=60, first=first)

    application.add_error_handler(error_handler)

    application.run_polling()

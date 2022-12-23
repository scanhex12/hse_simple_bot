import telebot
import torch
from transformers import pipeline
from transformers import T5ForConditionalGeneration, T5Tokenizer


tokenizer = T5Tokenizer.from_pretrained("cointegrated/rut5-small-chitchat")
model = T5ForConditionalGeneration.from_pretrained("cointegrated/rut5-small-chitchat")

generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
token = "5891090910:AAFCT8iIbvngT4W_OvaTKJ28yGWp9EnLPNA"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️ ")


@bot.message_handler(commands=['help'])
def start_message(message):
    help_text = """Если хотите пообщаться с ботом, введите generate+<text>
                   Чтобы получить случайную картинку, введите /pic
                   Чтобы получить тайный стикер, введите /sticker
                   Чтобы начать работу с ботом, нажмите /start
                   По любым непонятным вопросам - /help
                """
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['sticker'])
def send_sticker(message):
    bot.send_sticker(message.chat.id, "https://github.com/TelegramBots/book/raw/master/src/docs/sticker-fred.webp")


@bot.message_handler(commands=['pic'])
def send_photo(message):
    file = open('img.png', 'rb')
    bot.send_photo(chat_id=message.chat.id, photo=file)
    file.close()


def generate_text(text, max_length=30):
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        hypotheses = model.generate(
            **inputs,
            do_sample=True, top_p=0.5, num_return_sequences=1,
            repetition_penalty=2.5,
            max_length=32,
            min_length=10
        )
    for h in hypotheses:
        return tokenizer.decode(h, skip_special_tokens=True)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    generation_key = "generate"
    if message.text[:len(generation_key)] == generation_key:
        bot.reply_to(message, generate_text(message.text[len(generation_key):]))
        return
    generation_key = "сгенерируй"
    if message.text[:len(generation_key)] == generation_key:
        bot.reply_to(message, generate_text(message.text[len(generation_key):]))
        return


bot.polling()


from telebot import types
import requests, json
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, Filters, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


ESPERANDO_CIUDAD = 0


#mensaje bienvenida
def bienvenida (update, context):

    update.message.reply_text(
        text="Hola! 🥰 ¿En qué puedo ayudarte?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text= "Quiero saber el clima", callback_data='clima')],
            [InlineKeyboardButton(text="Quiero contar", callback_data='contar')]
        ])
    )


def clima (update, context):
    update.message.reply_text("De qué ciudad quieres saber el clima actual?")
    return ESPERANDO_CIUDAD

def func_aux_clima (update, context):
    query = update.callback_query
    query.answer() #respuesta invisible

    query.edit_message_text(text= "De qué ciudad quieres saber el clima actual?")

    return ESPERANDO_CIUDAD

def generarclima(ciudadsolicitada):
    # API CLIMA
    apikey = "785c7b7ee6436ccf98f14a65c8009947"
    lenguaje = "sp"
    respuesta_clima = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang={}".format(ciudadsolicitada, apikey, lenguaje))
    jsonrespuesta = respuesta_clima.text
    resp_dic = dict(json.loads(jsonrespuesta))

    #obtengo el valor de weather, que es una lista cuyo único elemento es un diccionario
    weather = resp_dic.get('weather')

    #guardo el diccionario en una variable
    dic_descripcion = weather[0]

    #accedo al campo 'descripción'
    datodescripcion = dic_descripcion.get('description')

    #repito para obtener la temperatura actual
    main = resp_dic.get('main')
    datotemperatura = main.get('temp')

    #lo mismo para la ciudad
    datociudad = resp_dic.get('name')

    respuesta_limpia = "🌤️ 🌧️ ☀️\nEl clima actual en {} es {} y la temperatura {} ºC\n 🌤️ 🌧️ ☀".format(datociudad, datodescripcion, datotemperatura)

    return respuesta_limpia

def enviarclima(respuesta_limpia,chat):
    chat.send_message(text=respuesta_limpia, timeout= None)

def ciudad (update, context):
    ciudadsolicitada = update.message.text

    respuesta = (generarclima(ciudadsolicitada))

    chat = update.message.chat

    enviarclima(respuesta, chat)

    return ConversationHandler.END

#falta función para contador


if __name__ == "__main__":
    updater: Updater = Updater(token="1721137347:AAGMaVZcrsY46jkybVJwhfPMqo_FwjOJhg4", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", bienvenida))


    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("clima", clima),
            CallbackQueryHandler(pattern='clima', callback=func_aux_clima)
            #CallbackQueryHandler(pattern='contar', callback=func_aux_contar)

        ],
        states={
            ESPERANDO_CIUDAD: [MessageHandler(Filters.text, ciudad)]
        },
        fallbacks=[])
    )

    #para escuchar mensajes
    updater.start_polling()
    updater.idle()




import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from register import     register_safa
import unicodedata
import re


def super_bot(TOKEN, bot_token ,chat_id):
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s -  %(message)s,")
    logger = logging.getLogger()

### 1 ENVIA EL STATUS DEL BOT 
    def getBotInfo(update, context):
        bot = context.bot
        chatId= update.message.chat_id

        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId) )
        print(context.args)
        
        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",text= f"Hola soy un bot creado para la Nave por Sr Spok. sigo funcionando no te preocupes❗❗❗ "
            #,message_thread_id="5"
        )



    ### 14 CREA HTML DE BUSQUEDA DE MARCA Y DSCT PERSONALIZADO
    def fazil_reg(update, context):
        user_id = update.message.from_user.id
        chat_id = update.message.chat_id
        message_text = update.message.text
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        bot = context.bot
       
        var = message_text
        var = var[2:]
        var = var.split()
     

        if len(var) < 4:
                bot.sendMessage(
            chat_id=chat_id,
            parse_mode="HTML",text= f"Faltan datos para crear la cuenta de fazil "
            #,message_thread_id="5"
             )

        name = (var[0])
        last_name= (var[1])

 
        normalizada = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
        normalizada2 = unicodedata.normalize('NFKD', last_name).encode('ASCII', 'ignore').decode('utf-8')
        if normalizada.isalpha() and normalizada2.isalpha():
            print("La cadena contiene solo letras (sin acentos)")
        else:
           bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Formato incorrecto: /f nombre appelido celular email"
                )
           name = None;last_name = None


       
        #dni=str(var[2])
        cel=str(var[2])
        if cel.isdigit() and len(cel) == 9:
            print("The string contains only numbers and 9 digits")
        else:
            bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Formato incorrecto: /f nombre appelido celular email, el celular solo debe tener 9 digitos"
                )
            cel = None
            


        email=str(var[3])
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if re.match(pattern, email):
            print("La dirección de correo electrónico es válida")
        else:
            bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Formato incorrecto: /f nombre appelido celular email, formato de email incorrecto"
                )
            email = None
        print(name)
        print(last_name)
        print(cel)
        print(email)
        #pwd=str(var[5])
        if name or last_name or cel or email == None:
            print(" error de data input")
        if name and last_name and cel and email != None:
            if user_id == 1160667522 or 1712594729:
                bot.sendMessage(
                    chat_id=chat_id,
                    parse_mode="HTML",text= f"Creando cuenta Fazil"
            
                    )
                try:
                    register_safa(name,last_name,cel,email)
                    bot.sendMessage(
                    chat_id=chat_id,
                    parse_mode="HTML",text= f"Usuario se creo exitosamente "
                    )
                except:
        
            
                    bot.sendMessage(
                    chat_id=chat_id,
                    parse_mode="HTML",text= f"Usuario ya existe o hubo error en el proceso "
            
                    )
            else:
                bot.sendMessage(
                    chat_id=chat_id,
                    parse_mode="HTML",text= f"Acceso Restringido, no estas autorizado a usar este comando"
            
                    )


      
       




    # if __name__ == "__main__":
    myBot = telegram.Bot(token = TOKEN)
    print(myBot.getMe())

    updater = Updater(myBot.token, use_context=True)

    dp= updater.dispatcher
    dp.add_handler(CommandHandler("botinfo", getBotInfo))

#

    dp.add_handler(CommandHandler("f", fazil_reg))


    updater.start_polling()
    updater.idle()
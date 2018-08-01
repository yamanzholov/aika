from weather_predict import *
import random
from classify import *
from translate import *
import telebot
from speech_to_text import *



token = '655665228:AAGfa7LvWw46UzckGEMbyG3HZ4-XTo3nQ0E'
answer = ["Привет!", "Здравствуй", "Приветствую!", "Здравствуйте"]
answer_greetings_mood = ["Привет. Пойдет. Как у тебя?", "Здравствуй. Хорошо. Как у тебя?", "Приветствую. Нормально. Как у тебя?", "Здарова. Неплохо. Как у тебя?", "Здравствуйте. Все отлично. Как у вас?"]
answer_mood = ["Замечательно, спасибо!!", "Хорошо. Как у тебя дела?", "Все нормально. Как у вас?", "Все отлично. Как у тебя?", "Пойдет. А у тебя?"]
answer_philosophy = ['42']
answer_action = ['Разговариваю с тобой', 'Существую', 'Тихо жду здесь пока у меня что-то спросят']
answer_status_good = ['Рада слышать', 'Круто', 'Отлично!', 'Я очень рада :)']
command = '1'
bot = telebot.TeleBot(token)
print("Программа запущена")

@bot.message_handler(content_types=["text","voice"])
def handle_message(message):
    if message.text:
        command = message.text
        try:
            predicted_class = classify(command)
            if(predicted_class == 'weather'):
                output, speech = get_weather(command)
                bot.send_message(message.chat.id, output)
            elif(predicted_class == 'greetings'):
                bot.send_message(message.chat.id, answer[random.randint(0,(len(answer)-1))])
            elif(predicted_class == 'greetings_mood'):
                bot.send_message(message.chat.id, answer_greetings_mood[random.randint(0,(len(answer_greetings_mood)-1))])
            elif(predicted_class == 'mood'):
                bot.send_message(message.chat.id, answer_mood[random.randint(0,(len(answer_mood)-1))])
            elif(predicted_class == 'philosophy'):
                bot.send_message(message.chat.id, answer_philosophy[0]) 
            elif(predicted_class == 'action'):
                bot.send_message(message.chat.id, answer_action[random.randint(0,(len(answer_action)-1))])
            elif(predicted_class == 'status_good'):
                bot.send_message(message.chat.id, answer_status_good[random.randint(0,(len(answer_status_good)-1))])
            # elif(predicted_class == 'translate'):
            #         bot.send_message(message.chat.id, print(translate(command)))
            else:
                bot.send_message(message.chat.id, 'Извините, я вас не понимаю, но я учусь :3')
        except:
            pass
    else:
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        try:
            command = speech_to_text(bytes=file.content)
        except:
            bot.send_message(message.chat.id, 'Распознование голоса не удалось, попробуйте снова')
        try:
            predicted_class = classify(command)
            if(predicted_class == 'weather'):
                output, speech = get_weather(command)
                speech_url = 'https://tts.voicetech.yandex.net/generate?text={}&format=mp3&quality=lo&lang=ru-RU&speaker=oksana&emotion=good&key=c3667808-f5a2-4c52-8f90-699a3e23e4f2'.format(speech)
                doc = requests.get(speech_url)
                with open('audio.ogg', 'rb') as f:
                    f.write(doc.content)
                voice = open('audio.ogg', 'rb')
                bot.send_message(message.chat.id, output)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'greetings'):
                bot.send_message(message.chat.id, answer[random.randint(0,(len(answer)-1))])
            elif(predicted_class == 'greetings_mood'):
                bot.send_message(message.chat.id, answer_greetings_mood[random.randint(0,(len(answer_greetings_mood)-1))])
            elif(predicted_class == 'mood'):
                bot.send_message(message.chat.id, answer_mood[random.randint(0,(len(answer_mood)-1))])
            elif(predicted_class == 'philosophy'):
                bot.send_message(message.chat.id, answer_philosophy[0]) 
            elif(predicted_class == 'action'):
                bot.send_message(message.chat.id, answer_action[random.randint(0,(len(answer_action)-1))])
            elif(predicted_class == 'status_good'):
                bot.send_message(message.chat.id, answer_status_good[random.randint(0,(len(answer_status_good)-1))])
            # elif(predicted_class == 'translate'):
            #         bot.send_message(message.chat.id, print(translate(command)))
            else:
                bot.send_message(message.chat.id, 'Извините, я вас не понимаю, но я учусь :3')
        except:
            pass



if __name__ == '__main__':
    bot.polling(none_stop=True)
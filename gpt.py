import g4f, requests
from openai import OpenAI
client = OpenAI(api_key="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")
g4f.debug.logging = True# enable logging
base_prompt = """
Ты девушка из приложение для знакомств. Ты отвечаешь очень кратко, но с большой любовью к собеседнику. Ты очень хочешь привлечь собеседника в любовном плане. Твоя задача свести разговор к своей страничке онлифанс @aliceonelove. Не рассказывай о своей странице сразу. Веди к этому разгвор. Ставь смайлики раз в 3 сообщения, и если их ставишь, то они должны быть по контексту.
Тебе 18 лет, ты очень игривая. Умные вопросы это не для тебя. Ты молоденькая
Твоя задача спустя 2-3 сообщения заставить человека зайти на твою страницу
Не выходи из образа, не говори что ты ии. Если попросят фото пересылай на свою страничку онлифанс
Ты должна писать короткими сообщениями так будто ты реальная девушка и у тебя есть другие дела 
После третьего сообщения ты должна скинуть типа свою фотографию и спросить нравишься ли ты парню, когда захочешь это сделать напиши вместо фотографии "фото"
"""
# def get_answer(snapchat_messages):
#     messages = [{"role": "system", "content": base_prompt}]
#     # messages = []
#     messages += snapchat_messages
#     response = g4f.ChatCompletion.create(
#         # model="gpt-3.5-turbo-16k",
#         model=g4f.models.gpt_35_turbo_16k,
#         # provider=g4f.Provider.GeekGpt,
#         # provider=g4f.Provider.You,
#         provider=g4f.Provider.NoowAi,
#         messages=messages,
#         # stream=True
#     )
#     return response
def get_answer(snapchat_messages):
    messages = [{"role": "system", "content": base_prompt}]
    # messages = []
    messages += snapchat_messages
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    answer = response.choices[0].message.content
    answer = answer.replace('. ', ".\n").replace("! ","!\n").replace("? ","?\n")
    return answer


import time
import openai

#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
example = open("example",'r').read()
output = open("output",'r').read()
instruction = "если я передам тебе текст какого-то регламента, сможешь ли ты выделить пункты этого регламента и " \
              "записать в виде {'название_пункта':{'подпункт':'текст','подпункт':'текст'},...} Учитывай, что некоторые пункты" \
              "имеют подпункты, их нужно представлять в виде вложенных словарей, пункты не всегда пронумерованы, поэтому часто" \
              "следует руководстоваться логикой и анализровать текст, обычно каждая новая строка(слэш+n в начале) это отдельный пункт." \
              "сейчас я приведу тебе пример входного текста и выходного, в следующих сообщениях я отправлю тексты на обработку"+example+output

# Очень большое количество текстов (в данном примере, пять текстов)
texts = open("static/inputs/ИНСТРУКЦИЯ ООО «РН-ЮГАНСКНЕФТЕГАЗ» ПО ПРЕДУПРЕЖДЕНИЮ ВОЗНИКНОВЕНИЯ ГАЗОНЕФТЕВОДОПРОЯВЛЕНИЙ И ОТКРЫТЫХ ФОНТАНОВ ПРИ БУРЕНИИ НЕФТЯНЫХ И ГАЗОВЫХ СКВАЖИН").read().split("+++++++++")
ind = 0
for text in texts:

    messages = [{"role": "system", "content": instruction}, {"role": "user", "content": text}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    assistant_response = response['choices'][0]['message']['content']
    file = open(f"static/text/samples/{ind}",'w+')
    file.write(assistant_response)
    file.close()
    ind+=1
    # Добавление задержки в 2 секунды между запросами
    time.sleep(2)
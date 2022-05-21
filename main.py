import lexerProg

while True:
    text = input('Текст: ')
    if text == 'exit':
        print('Конец программыы.')
        exit()
    result = lexerProg.run(text)

    print(result)
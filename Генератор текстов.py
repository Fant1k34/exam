class TextGenerator:
    def __init__(self):
        print("Здравствуйте, вы используете версию генератора текста")
        print("Вызовите метод help() для получения информации по командам")
        self.words = []
        
        
    def help(self):
        print("fit(path) - использовать текст, находящийся по пути path для обучения модели")
        print("generate(n=..., first=...) - сгенирировать предложение из n слов")
        print("Первым словом будет first. Оба аргумента - необязательные. Тогда слово и n будет выбрано случайно")
        print("clear() - очистить полностью память модели")
    
    
    def fit(self, path):
        import random
        self.sl = dict()
        with open("know.txt") as file:         # Считываем информацию о всех изученных словах
            lines = file.read().split("\n")
            for el in lines:
                if el == "":
                    continue
                self.sl[el.split()[0]] = el.split()[1:]
        with open(path, 'r') as file:
            text = file.read().replace(",", "").replace(".", "\t").replace(":", "\t").replace("!", "\t").replace("?", "\t").replace(";", "\t").replace("\n", "\t").replace("–", "\t").replace("…", "\t").lower().split("\t") #Избавляемся от запятых. Знаки .:!?; заменяем тем, чем будем дальше делить предложения, так как через точку или восклицательный знак могут стоять НЕСВЯЗНЫЕ слова! 
        
        for el in text:
            words = el.split() # word - список слов предложения
            for i in range(len(words) - 1): # Для каждого слова добавляем следующее слово. СЛОВА БУДУТ ПОВТОРЯТЬСЯ. Таким образом шанс  сгенерировать более употребляемое слово гораздо выше!
                self.sl[words[i]] = self.sl.get(words[i], []) + [words[i+1]]
                self.words.append(words[i])
        
        with open("know.txt", "a") as file: # Записываем словарь в нужном нам виде:
                                            # Ключ_слова_которые_идут_дальше
            answ = ""
            for (key, value) in self.sl.items():
                answ += key
                answ += " "
                answ += " ".join(value)
                answ += "\n"
            file.write(answ)
            
        with open("words.txt", "a") as file:
            file.write(" ".join(self.words))
    
    
    def generate(self, n=-1, first=""):  
        try:
            import random                         # Ниже записываем все слова, которые мы знаем
            with open("words.txt", "r") as file:  # в список и словарь
                self.words = file.read().split()
            if n < 0 or type(n) != int:
                n = random.choice(range(1,10))    # Определяемся с параметрами
            self.sl = dict()  
            with open("know.txt") as file:        # Получаем наш словарь
                lines = file.read().split("\n")
                for el in lines:
                    if el == "":
                        continue
                    self.sl[el.split()[0]] = el.split()[1:]
            if first == "":
                first = random.choice(self.words)
            sent = []
            for (key, value) in self.sl.items():  # Сам механизм генерации последовательности.
                if key == first:
                    next_word = first
                    while n>0:
                        sent.append(next_word)
                        n -= 1
                        next_word = random.choice(self.sl.get(key))
                    break
            print(" ".join(sent).capitalize() + ".")
        except Exception:
            print("Произошла ошибка. Возможно, вы не обучили модель совсем!")
    
    
    def clear(self):
        with open("know.txt", "w") as file:
            self.sl = dict()
            self.words = []
        with open("words.txt", "w") as file:
            pass
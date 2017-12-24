from random import randint, choice


class Ore:
    def __init__(self, number, total_ore):
        self.number = number
        self.total_ore = total_ore

    def pick_ore(self, number):
        if self.total_ore < number:
            print('Такого количества руды в жиле нет')
            return False
        self.total_ore -= number
        return True

    def status(self):
        print('Жила номер {number}, руды: {ore}'.format(number=self.number, ore=self.total_ore))


class Mine:
    def __init__(self, name, ore_count=10):
        self.name = name
        self.miners = []
        self.ore_list = []
        self.init_ore(ore_count)

    def init_ore(self, count):
        for i in range(count):
            ore = Ore(number=i + 1, total_ore=randint(100, 200))
            self.ore_list.append(ore)
        print('В шахте создано {count} рудных жил'.format(count=len(self.ore_list)))

    def log_miner(self, miner):
        print('В шахту зашел рудокоп {name}'.format(name=miner.name))
        self.miners.append(miner)

    def status(self):
        print('В шахте {name} находится {count} рудокопов, жил: {ores}'.format(
            name=self.name, count=len(self.miners), ores=len(self.ore_list)
        ))


class Shop:
    def __init__(self, name):
        self.name = name
        self.price = 5

    def log_shoping(self, miner):
        print('В магазин зашел рудокоп {name}'.format(name=miner.name))




class Miner:
    def __init__(self, name):
        self.name = name
        self.ore = 10
        self.mine = None
        self.has_pickaxe = False
        self.skill = 20
        self.health = 100
        self.is_dead = False
        self.have_dinner = 0

    def status(self):
        print('Навык рудокопа: {skill}'.format(skill=self.skill))
        print('У рудокопа {name} {health} очков жизни'.format(name=self.name, health=self.health))
        print('У рудокопа {name} припасено {count} обедов'.format(name=self.name, count=self.have_dinner))

    def who_am_i(self):
        print('Я - рудокоп {name}, у меня {ore} руды'.format(name=self.name, ore=self.ore))
        alef.status()
        if self.mine:
            print('Я работаю в шахте {name}'.format(name=self.mine.name))
        else:
            print('Я безработный :(')

    def calculate_punch(self, ore):
        chance = randint(1, 100)
        if chance > self.skill:
            return 0
        return randint(5, 15)

    def check_health(self):
        chance_tired = randint(1, 100)
        tired = randint(1, 5)
        very_tired = randint(5, 15)
        if self.health > 0:
            if chance_tired > 70:
                print('Алефу повезло - он устраивал передышки во время работы и он не очень сильно устал')
                self.health -= tired
            else:
                print('Алеф трудился на шахте и это не самым лучшим образом сказалось на его здоровье')
                self.health -= very_tired
        else:
            self.is_dead = True
        return


    def skilling(self, ore_to_pick):
        chance_skill = randint(1, 100)
        if ore_to_pick > 1:
            if chance_skill > 40:
                if self.skill < 100:
                    self.skill += 1
                    print('Я выучил пару новых приемов добычи')
                    return
            if self.skill >99:
                print('Я - мастер среди рудокопов. Мне больше нечему тут учиться')
            else:
                print('Не смог научиться ничему новому')
        return

    def choice_ore(self):
        ore = choice(self.mine.ore_list)
        print('Выбрал жилу')
        ore.status()
        return ore

    def mine_ore(self):
        if self.mine:
            if self.has_pickaxe:
                ore = self.choice_ore()
                print('Приступил к добыче')
                ore_to_pick = self.calculate_punch(ore)
                self.check_health()
                if ore_to_pick < 1:
                    print('Добыть ничего не удалось')
                    return
                if ore.pick_ore(ore_to_pick):
                    self.ore += ore_to_pick
                    print('Добыто {ore} руды'.format(ore=ore_to_pick))
                    self.skilling(ore_to_pick)
                else:
                    print('Жила пуста, добыть не удалось')
            else:
                print('Не могу работать, нет кирки')
        else:
            print('Не могу работать, нахожусь не в шахте')

    def shoping(self):
        price = shop.price
        if self.ore >= price:
            self.ore -= price
            print('Рудокоп Алеф купил себе обед')
            self.have_dinner += 1
        else:
            print('Алеф с завистью смотрел на вкусные обеды, но увы был вынужден уйти из магазина с пустым желудком:(')

    def rest(self):
        chance_healing = randint(20, 30)
        if self.have_dinner:
            print('Надо бы подкрепиться')
            self.have_dinner -= 1
            self.health += chance_healing
        print('Я весь день пинал балду')

    def go_to_mine(self, mine):
        self.mine = mine
        self.mine.log_miner(self)

    def go_shoping(self, shop):
        self.shop = shop
        self.shop.log_shoping(self)

    def pick_pickaxe(self):
        if self.mine:
            print('[{name}] Мне выдали кирку'.format(name=self.name))
            self.has_pickaxe = True
        else:
            print('Негде взять кирку, нахожусь не в шахте')

    def act(self):
        dice = randint(1, 6)
        if dice > 4 and self.have_dinner < 5:
            self.shoping()
        elif self.have_dinner > 0 and self.health < 50:
            self.rest()
        else:
            self.mine_ore()


shop = Shop('Лавка Декстера')

old_mine = Mine('Старая шахта', ore_count=50)
old_mine.status()

alef = Miner('Алеф')
alef.who_am_i()
alef.mine_ore()

alef.go_to_mine(old_mine)
old_mine.status()

alef.mine_ore()

alef.pick_pickaxe()
alef.who_am_i()

for i in range(70):
    print('++++ Наступил новый день: {day}'.format(day=i + 1))
    if alef.is_dead:
        print('Мертвые не могут добывать руду')
        break
    alef.act()
    alef.who_am_i()
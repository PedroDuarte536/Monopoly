from random import randint

class Dice:
    def __init__(self, max_value):
        self.max_value = max_value

    def roll(self):
        value = randint(1, self.max_value)
        return value

class Table:
    def __init__(self, houses):
        self.houses = houses

class Player:
    def __init__(self, character, ini_money):
        self.character = character
        self.money = ini_money
        self.pos = 0
        self.playing = True

class House:
    def __init__(self, name, price, group):
        self.name = name
        self.price = price
        self.group = group
        self.owner = -1
        self.houses = 0
        self.hyp = False
        self.exchange = 0
        self.sell = 0

class House_Group:
    def __init__(self, house, rent, hyp):
        self.house = house
        self.rent = rent
        self.hyp = hyp
        self.num_houses = 0

    def increment_num_houses(self):
        self.num_houses += 1

class Game:
    def __init__(self, houses=0, houses_groups=0, ini_money=0, players=0):
        if houses != 0 and houses_groups != 0 and ini_money != 0 and players != 0:
            self.prepare_table(houses, houses_groups)
            self.prepare_players(ini_money, players)

    def create_house_group(self, house, rent, hyp):
        result = House_Group(house, rent, hyp)
        return result
        
    def create_house(self, name, price, rent):
        result = House(name, price, rent)
        return result
        
    def prepare_table(self, houses, house_groups):
        self.house_groups = []
        self.houses = []

        for group in house_groups:
            new_group = self.create_house_group(group['house'], group['rent'], group['hypothec'])
            self.house_groups.append(new_group)
            
        new_house = self.create_house("START", "0", "0")
        self.houses.append(new_house)
            
        for house in houses:
            new_house = self.create_house(house['name'], house['price'], house['group'])
            self.houses.append(new_house)
            self.house_groups[house['group']].increment_num_houses()

        self.table = Table(self.houses)
        

    def create_player(self, character, ini_money):
        result = Player(character, ini_money)
        return result
    
    def prepare_players(self, ini_money, players):
        self.players = []

        for player in players:
            new_player = self.create_player(player['name'], ini_money)
            self.players.append(new_player)
        

    def game_cycle(self):
        self.play = True
        self.dice = Dice(6)

        while self.play:
            for player in self.players:
                if player.playing:
                    print(player.character + "'s Turn...")

                    dice_value = self.dice.roll()
                    player.pos += dice_value

                    while player.pos > len(self.houses)-1:
                        player.pos -= len(self.houses)
                        player.money += 2000

                    print("Money: " + str(player.money) + "$")
                    print("Pos: " + str(self.houses.index(self.houses[player.pos])) + " - " + self.houses[player.pos].name + "(" + str(dice_value) + ")")

                    if player.pos != 0:
                        if self.houses[player.pos].owner == -1:
                            if player.money >= self.houses[player.pos].price:
                                if input("Want To Buy '" + self.houses[player.pos].name + "'? (" + str(self.houses[player.pos].price) + "$ - " + str(self.house_groups[self.houses[player.pos].group].rent[self.houses[player.pos].houses]) + "$)") == "S":
                                    self.houses[player.pos].owner = self.players.index(player)
                                    player.money -= self.houses[player.pos].price

                                    print("Purchase Completed")

                                else:
                                    print("Purchase Passed")
                            else:
                                print("Not Enough Money To Purchase")
                        else:
                            if self.houses[player.pos].owner == self.players.index(player):
                                print(self.houses[player.pos].name + " Is Already Yours")
                                
                            elif self.houses[player.pos].hyp:
                                print("You Won't Pay To " + self.players[self.houses[player.pos].owner].character + " Because It Is Hypothecated")

                            elif player.money >= self.house_groups[self.houses[player.pos].group].rent[self.houses[player.pos].houses]:
                                player.money -= self.house_groups[self.houses[player.pos].group].rent[self.houses[player.pos].houses]
                                self.players[self.houses[player.pos].owner].money += self.house_groups[self.houses[player.pos].group].rent[self.houses[player.pos].houses]

                                print("You Payed " + str(self.house_groups[self.houses[player.pos].group].rent[self.houses[player.pos].houses]) + "$ To " + self.players[self.houses[player.pos].owner].character + " As Rent")

                            else:
                                self.players[self.houses[player.pos].owner].money += player.money

                                print("You Payed " + str(player.money) + "$ Instead Of " + str(self.house_groups[self.houses[player.pos].group].rent[self.houses[player.pos].houses]) + "$ To " + self.players[self.houses[player.pos].owner].character + " As Rent And You're Out")

                                player.money = 0
                                player.playing = False

                    action_entered = False
                    while not action_entered:
                        print("1) Hypothecate")
                        print("2) Build Houses")
                        print("3) Sell/Buy")
                        print("4) Pass")
                        action = input("> ")

                        if action == '1':
                            usr_houses = []
                            for house in self.houses:
                                if house.owner == self.players.index(player):
                                    usr_houses.append(house)

                            if len(usr_houses) > 0:
                                i = 0
                                for house in usr_houses:
                                    print(str(i+1) + ") " + house.name, end='')
                                    i += 1
                                    if house.hyp:
                                        print("*")
                                    else:
                                        print()

                                print(str(i+1) + ") Back")

                                house_selected = False
                                while not house_selected:
                                    select = int(input("> ")) - 1

                                    if select >= 0 and select <= len(usr_houses):
                                        if select == len(usr_houses):
                                            house_selected = True
                                        else:
                                            if usr_houses[select].hyp:
                                                if player.money >= self.house_groups[self.houses[self.houses.index(usr_houses[select])].group].hyp:
                                                    player.money -= self.house_groups[self.houses[self.houses.index(usr_houses[select])].group].hyp
                                                    usr_houses[select].hyp = False
                                                    house_selected = True
                                                else:
                                                    print("Not Enough Money!")
                                            else:
                                                player.money += self.house_groups[self.houses[self.houses.index(usr_houses[select])].group].hyp
                                                usr_houses[select].hyp = True
                                                house_selected = True
                                    
                        elif action == '2':
                            usr_houses = []
                            groups_count = {}
                                
                            for house in self.houses:
                                if house.owner == self.players.index(player):
                                    if house.group in groups_count:
                                        groups_count[house.group] += 1
                                    else:
                                        groups_count[house.group] = 1
                                    
                            for house in self.houses:
                                if house.owner == self.players.index(player):
                                    if groups_count[house.group] == self.house_groups[house.group].num_houses:
                                        usr_houses.append(house)

                            if len(usr_houses) > 0:
                                i = 0
                                for house in usr_houses:
                                    print(str(i+1) + ") " + house.name + " - " + str(house.houses))
                                    i += 1

                                print(str(i+1) + ") Back")

                                house_selected = False
                                while not house_selected:
                                    select = int(input("> ")) - 1

                                    if select >= 0 and select <= len(usr_houses):
                                        if select == len(usr_houses):
                                            house_selected = True
                                        else:
                                            if usr_houses[select].houses < len(self.house_groups[usr_houses[select].group].rent)-1:
                                                if player.money >= self.house_groups[usr_houses[select].group].house:
                                                    player.money -= self.house_groups[usr_houses[select].group].house
                                                    usr_houses[select].houses += 1
                                                    house_selected = True
                                                else:
                                                    print("Not Enough Money!")
                                            else:
                                                print("House Can't Have More Houses!")
                                                
                        elif action == '3':
                            option_chosen = False
                            while not option_chosen:
                                print("1) Sell")
                                print("2) Exchange")
                                print("3) Buy")
                                print("4) Back")

                                option = input("> ")

                                if option == '1':
                                    usr_houses = []
                                    for house in self.houses:
                                        if house.owner == self.players.index(player):
                                            usr_houses.append(house)

                                    if len(usr_houses) > 0:
                                        i = 0
                                        for house in usr_houses:
                                            print(str(i+1) + ") " + house.name, end='')
                                            i += 1
                                            if house.sell != 0:
                                                print(" (" + str(house.sell) + ")")
                                            else:
                                                print()

                                        print(str(i+1) + ") Back")

                                        house_selected = False
                                        while not house_selected:
                                            select = int(input("> ")) - 1

                                            if select >= 0 and select <= len(usr_houses):
                                                if select == len(usr_houses):
                                                    house_selected = True
                                                else:
                                                    if usr_houses[select].sell != 0:
                                                        self.houses[self.houses.index(usr_houses[select])].sell = 0
                                                    else:
                                                        amount = int(input("How Much Do You Want For " + usr_houses[select].name + "? "))
                                                        if amount > 0:
                                                            self.houses[self.houses.index(usr_houses[select])].sell = amount
                                                        else:
                                                            print("Please Enter A Valid Amount!")
                                                    house_selected = True
                                            
                                elif option == '2':
                                    usr_houses = []
                                    for house in self.houses:
                                        if house.owner == self.players.index(player):
                                            usr_houses.append(house)

                                    if len(usr_houses) > 0:
                                        i = 0
                                        for house in usr_houses:
                                            print(str(i+1) + ") " + house.name, end='')
                                            i += 1
                                            if house.exchange != 0:
                                                print(" (" + str(self.houses[house.exchange].name) + ")")
                                            else:
                                                print()

                                        print(str(i+1) + ") Back")

                                        house_selected = False
                                        while not house_selected:
                                            select = int(input("> ")) - 1

                                            if select >= 0 and select <= len(usr_houses):
                                                if select == len(usr_houses):
                                                    house_selected = True
                                                else:
                                                    if usr_houses[select].exchange != 0:
                                                        self.houses[self.houses.index(usr_houses[select])].exchange = 0
                                                    else:
                                                        owned_houses = []
                                                        for house in self.houses:
                                                            if house.owner != -1 and house.owner != self.players.index(player):
                                                                owned_houses.append(house)

                                                        if len(owned_houses) > 0:
                                                            i = 0
                                                            for house in owned_houses:
                                                                print(str(i+1) + ") " + house.name + " (" + str(house.price) + "$ - " + str(self.house_groups[house.group].rent[0]) + "$)")
                                                                i += 1
                                                                
                                                            print(str(i+1) + ") Back")

                                                            ex_selected = False
                                                            while not ex_selected:
                                                                ex_select = int(input("> ")) - 1
                                                                if ex_select > 0 and ex_select <= len(owned_houses)+1:
                                                                    if ex_select == len(owned_houses)+1:
                                                                        house_selected = True
                                                                    else:
                                                                        usr_houses[select].exchange = self.houses.index(owned_houses[ex_select])

                                                                ex_selected = True
                                                    house_selected = True
                                        
                                        
                                elif option == '3':
                                    for_sale_houses = []
                                    for house in self.houses:
                                        if house.sell > 0 and house.owner != self.players.index(player):
                                            for_sale_houses.append(house)
                                            
                                    for_exchange_houses = []
                                    for house in self.houses:
                                        if self.houses[house.exchange].owner == self.players.index(player):
                                            for_exchange_houses.append(house)

                                    if len(for_sale_houses) > 0 or len(for_exchange_houses) > 0:
                                        i = 0
                                        for house in for_sale_houses:
                                            print(str(i+1) + ") " + house.name + " (" + str(house.sell) + ")", end='')
                                            i += 1
                                            if house.hyp:
                                                print(" - Hypothecated (" + self.house_groups[house.group].hyp + "$)")
                                            else:
                                                print()
                                        
                                        for house in for_exchange_houses:
                                            print(str(i+1) + ") " + house.name + " (" + str(house.price) + "$ - " + str(self.house_groups[house.group].rent[0]) + "$) For " + self.houses[house.exchange].name + " (" + str(self.houses[house.exchange].price) + "$ - " + str(self.house_groups[self.houses[house.exchange].group].rent[0]) + "$)", end='')
                                            i += 1
                                            if house.hyp:
                                                print(" - Hypothecated (" + self.house_groups[house.group].hyp + "$)")
                                            else:
                                                print()
                                            
                                        print(str(i+1) + ") Back")

                                        house_selected = False
                                        while not house_selected:
                                            select = int(input("> ")) - 1

                                            if select >= 0 and select < len(for_sale_houses):
                                                if player.money >= for_sale_houses[select].sell:
                                                    self.players[self.houses[self.houses.index(for_sale_houses[select])].owner].money += for_sale_houses[select].sell
                                                    player.money -= for_sale_houses[select].sell
                                                    self.houses[self.houses.index(for_sale_houses[select])].sell = 0
                                                    self.houses[self.houses.index(for_sale_houses[select])].owner = self.players.index(player)
                                                    self.houses[self.houses.index(for_sale_houses[select])].houses = 0
                                                    self.houses[self.houses.index(for_sale_houses[select])].exchange = 0
                                                    house_selected = True
                                                else:
                                                    print("Not Enough Money!")
                                                    house_selected = True

                                            elif select >= len(for_sale_houses) and select <= len(for_sale_houses) + len(for_exchange_houses):
                                                if select == len(for_sale_houses) + len(for_exchange_houses):
                                                    house_selected = True
                                                else:
                                                    if not for_exchange_houses[select-len(for_sale_houses)].hyp:
                                                        self.houses[for_exchange_houses[select-len(for_sale_houses)].exchange].sell = 0
                                                        self.houses[for_exchange_houses[select-len(for_sale_houses)].exchange].owner = for_exchange_houses[select-len(for_sale_houses)].owner
                                                        self.houses[for_exchange_houses[select-len(for_sale_houses)].exchange].houses = 0
                                                        self.houses[for_exchange_houses[select-len(for_sale_houses)].exchange].exchange = 0
                                                        
                                                        self.houses[self.houses.index(for_exchange_houses[select-len(for_sale_houses)])].sell = 0
                                                        self.houses[self.houses.index(for_exchange_houses[select-len(for_sale_houses)])].owner = self.players.index(player)
                                                        self.houses[self.houses.index(for_exchange_houses[select-len(for_sale_houses)])].houses = 0
                                                        self.houses[self.houses.index(for_exchange_houses[select-len(for_sale_houses)])].exchange = 0
                                                        house_selected = True
                                                    else:
                                                        print("Not Enough Money!")
                                                        house_selected = True
                                                
                                            
                                elif option == '4':
                                    option_chosen = True
                                            
                        elif action == '4':
                            action_entered = False
                            break
                        else:
                            print("Invalid Input!")
                                
                            
                
            

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
    def __init__(self, name, price, rent):
        self.name = name
        self.price = price
        self.rent = rent
        self.owner = -1

class Game:
    def __init__(self, houses=0, houses_groups=0, ini_money=0, players=0):
        if houses != 0 and houses_groups != 0 and ini_money != 0 and players != 0:
            self.house_groups = houses_groups
            self.houses = []

            new_house = self.create_house("START", "0", "0")
            self.houses.append(new_house)
            
            for house in houses:
                new_house = self.create_house(house['name'], house['price'], houses_groups[house['group']]['rent'])
                self.houses.append(new_house)

            self.table = Table(self.houses)
            
            self.players = []

            for player in players:
                new_player = self.create_player(player['name'], ini_money)
                self.players.append(new_player)

        else:        
            self.prepare_table()
            self.prepare_players()

            self.game_cycle()
        
    def create_house(self, name, price, rent):
        result = House(name, price, rent)
        return result
        
    def prepare_table(self):
        self.houses = []
        self.stop_cycle = False

        new_house = self.create_house("START", "0", "0")
        self.houses.append(new_house)
        
        while not self.stop_cycle:
            house_name = input("House Name: ")
            house_price = input("House Price: ")
            house_rent = input("House Rent: ")

            new_house = self.create_house(house_name, house_price, house_rent)
            self.houses.append(new_house)

            if input("Add More?(S/N) ") == "N":
                self.stop_cycle = True

        self.table = Table(self.houses)

    def create_player(self, character, ini_money):
        result = Player(character, ini_money)
        return result
    
    def prepare_players(self):
        self.players = []
        self.stop_cycle = False

        ini_money = input("Initial Money For Players: ")
        while not self.stop_cycle:
            player_name = input("Player's Name: ")

            new_player = self.create_player(player_name, ini_money)
            self.players.append(new_player)

            if input("Add More?(S/N) ") == "N":
                self.stop_cycle = True

    def game_cycle(self):
        self.play = True
        self.dice = Dice(6)

        while self.play:
            for player in self.players:
                if player.playing:
                    print(player.character + "'s Turn...")  
                    print("Money: " + str(player.money) + "$")

                    dice_value = self.dice.roll()
                    player.pos += dice_value

                    while player.pos > len(self.houses)-1:
                        player.pos -= len(self.houses)
                        player.money += 2000

                    print("Pos: " + str(self.houses.index(self.houses[player.pos])) + " - " + self.houses[player.pos].name + "(" + str(dice_value) + ")")

                    if player.pos != 0:
                        if self.houses[player.pos].owner == -1:
                            if player.money >= self.houses[player.pos].price:
                                if input("Want To Buy '" + self.houses[player.pos].name + "'? (" + str(self.houses[player.pos].price) + "$ - " + str(self.houses[player.pos].rent) + "$)") == "S":
                                    self.houses[player.pos].owner = self.players.index(player)
                                    player.money -= self.houses[player.pos].price

                                    print("Purchase Completed")

                                else:
                                    print("Purchase Passed")
                            else:
                                print("Not Enough Money To Purchase")
                        else:
                            if player.money >= self.houses[player.pos].rent:
                                player.money -= self.houses[player.pos].rent
                                self.players[self.houses[player.pos].owner].money += self.houses[player.pos].rent

                                print("You Payed " + str(self.houses[player.pos].rent) + "$ To " + self.players[self.houses[player.pos].owner].character + " As Rent")

                            else:
                                self.players[self.houses[player.pos].owner].money += player.money

                                print("You Payed " + str(player.money) + "$ Instead Of " + str(self.houses[player.pos].rent) + "$ To " + self.players[self.houses[player.pos].owner].character + " As Rent And You're Out")

                                player.money = 0
                                player.playing = False
                                
                            
                
            

from main import Game

houses = [{'name':'Campo Grande', 'price':600, 'group':0},
          {'name':'Avenida Fernão de Magalhães', 'price':600, 'group':0},
          {'name':'Avenida Almirante Reis', 'price':1000, 'group':1},
          {'name':'Avenida Luísa Todi', 'price':1000, 'group':1},
          {'name':'Avenida 24 de Julho', 'price':1200, 'group':1},
          {'name':'Avenida dos Combatentes', 'price':1400, 'group':2},
          {'name':'Rua Ferreira Borges', 'price':1400, 'group':2},
          {'name':'Avenida de Roma', 'price':1600, 'group':2},
          {'name':'Avenida da Boavista', 'price':1800, 'group':3},
          {'name':'Avenida da República', 'price':1800, 'group':3},
          {'name':'Rua de Sá da Bandeira', 'price':2000, 'group':3},
          {'name':'Rua de Santa Catarina', 'price':2200, 'group':4},
          {'name':'Rua do Carmo', 'price':2200, 'group':4},
          {'name':'Av. Marechal Gomes da Costa', 'price':2400, 'group':4},
          {'name':'Rua de Sto. António', 'price':2600, 'group':5},
          {'name':'Rua Garrett', 'price':2600, 'group':5},
          {'name':'Avenida dos Aliados', 'price':2800, 'group':5},
          {'name':'Avenida da Liberdade', 'price':3000, 'group':6},
          {'name':'Praça da Liberdade', 'price':3000, 'group':6},
          {'name':'Rua do Ouro', 'price':3200, 'group':6},
          {'name':'Rua Augusta', 'price':3500, 'group':7},
          {'name':'Rossio', 'price':4000, 'group':7}]

groups = [{'house':500, 'rent':[50, 300, 1000, 2000, 3500], 'hypothec':300},
          {'house':500, 'rent':[100, 500, 1500, 3000, 5000], 'hypothec':600},
          {'house':1000, 'rent':[150, 700, 2000, 4500, 7500], 'hypothec':1000},
          {'house':1000, 'rent':[200, 1000, 2500, 5000, 10000], 'hypothec':1400},
          {'house':1500, 'rent':[250, 1300, 3000, 6000, 15000], 'hypothec':1800},
          {'house':1500, 'rent':[300, 1500, 3500, 7000, 18000], 'hypothec':2500},
          {'house':2000, 'rent':[350, 2000, 4000, 8000, 2000], 'hypothec':3000},
          {'house':2000, 'rent':[500, 2500, 5000, 10000, 25000], 'hypothec':4000}]

ini_money = 2000

players = [{'name':'Jorge'}, {'name':'Mikel'}, {'name':'Amilcar'}]

teste = Game(houses, groups, ini_money, players)

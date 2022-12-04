from pprintpp import pprint as pp
from db.database import Graph


class FootballDAO(object):
    def __init__(self):
        self.db = Graph(uri='bolt://3.82.215.2:7687',
                        user='neo4j', password='liters-valley-bypass')

    def create_player(self, player):
        return self.db.execute_query('CREATE (n:Player {name:$name, age:$age, health:$health}) return n',
                                     {'name': player['name'], 'age': player['age'],'health': player['health']})

    def create_team(self, team):
        return self.db.execute_query('CREATE (n:Team {name:$name, coach:$coach, wins:$wins}) return n',
                                     {'name': team['name'], 'coach': team['coach'], 'wins': team['wins']})

    def read_by_name(self, player):
        return self.db.execute_query('MATCH (n:Player {name:$name}) RETURN n',
                                     {'name': player['name']})

    def read_by_name(self, team):
        return self.db.execute_query('MATCH (n:Team {name:$name}) RETURN n',
                                     {'name': team['name']})
    
    def read_all_nodes(self):
        return self.db.execute_query('MATCH (n) RETURN n')

    def update_health(self, player):
        return self.db.execute_query('MATCH (n:Player {name:$name}) SET n.health = $health RETURN n',
                                     {'name': player['name'], 'health': player['health']})

    def update_wins(self, team):
        return self.db.execute_query('MATCH (n:Team {name:$name}) SET n.wins = $wins RETURN n',
                                     {'name': team['name'], 'wins': team['wins']})

    def delete(self, player):
        return self.db.execute_query('MATCH (n:Player {name:$name}) DELETE n',
                                     {'name': player['name']})

    def delete_all_nodes(self):
        return self.db.execute_query('MATCH (n) DETACH DELETE n')

    def create_relation(self, player, team, year):
        return self.db.execute_query('MATCH (n:Player {name:$name}), (m:Team {name:$name}) CREATE (n)-[r:PLAYS_FOR{year: $year}]->(m) RETURN n, r, m',
                                     {'name': player['name'], 'name': team['name'], 'year': year})

    def read_relation(self, player, team, year):
        return self.db.execute_query('MATCH (n:Player {name:$name})-[r]->(m:Team {name:$name}) RETURN n, r, m',
                                     {'name': player['name'], 'name': team['name']})

def divider():
    print('\n' + '-' * 80 + '\n')

dao = FootballDAO()

while 1:    
    option = input('\n1. Create a player\n2. Create a team\n3. Read everything\n4. Update player health\n5. Delete a player\n6. Delete everything\n')

    if option == '1':
        name = input('  Name: ')
        age = input('   Age: ')
        health = input('  Health: ')
        player = {
            'name': name,
            'age': age,
            'health': health
        }
        aux = dao.create_player(player)
        divider()

    elif option == '2':
        name = input('  Name: ')
        coach = input('   Coach: ')
        wins = input('  Wins: ')
        team = {
            'name': name,
            'coach': coach,
            'wins': wins
        }
        aux = dao.create_team(team)
        divider()

    elif option == '3':
        aux = dao.read_all_nodes()
        pp(aux)
        divider()

    elif option == '4':
        name = input('  Name: ')
        health = input('   Health: ')
        person = {
            'name': name,
            'health': health
        }
        aux = dao.update_health(player)
        divider()

    elif option == '5':
        name = input('  Name: ')
        person = {
            'name': name
        }
        aux = dao.delete(player)
        divider()

    elif option == '6':
        aux = dao.delete_all_nodes()
        pp(aux)
        divider()

    else:
        break

dao.db.close()
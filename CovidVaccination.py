import argparse
import mysql.connector

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--username', required=True)
  parser.add_argument('--password', required=True)
  parser.add_argument('--action', required=True, choices=['login', 'signup', 'search', 'apply', 'add', 'get'])
  parser.add



def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--username', required=True)
  parser.add_argument('--password', required=True)
  parser.add_argument('--action', required=True, choices=['login', 'signup', 'search', 'apply', 'add', 'get'])
  parser.add_argument('--location', required=False)
  parser.add_argument('--center_id', required=False)
  parser.add_argument('--name', required=False)
  parser.add_argument('--capacity', required=False)
  parser.add_argument('--role', required=False)
  return vars(parser.parse_args())

def login(conn, username, password):
  cursor = conn.cursor()
  query = 'SELECT role FROM users WHERE username = %s AND password = %s'
  cursor.execute(query, (username, password))
  role = cursor.fetchone()
  if role:
    return role[0]
  else:
    return None

def signup(conn, username, password, role):
  cursor = conn.cursor()
  query = 'INSERT INTO users (username, password, role) VALUES (%s, %s, %s)'
  cursor.execute(query, (username, password, role))
  conn.commit()

def search_centers(conn, location):
  cursor = conn.cursor()
  query = 'SELECT name FROM centers WHERE location = %s'
  cursor.execute(query, (location,))
  centers = cursor.fetchall()
  return [center[0] for center in centers]

def apply_vaccination(conn, center_id):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) FROM dosages WHERE center_id = %s AND date = CURDATE()'
  cursor.execute(query, (center_id,))
  count = cursor.fetchone()[0]
  if count < 10:
    query = 'INSERT INTO dosages (center_id, date, dosage) VALUES (%s, CURDATE(), 1)'
    cursor.execute(query, (center_id,))
    conn.commit()
    return True
  else:
    return False

def add_center(conn, name, location, capacity):
  cursor = conn.cursor()
  query = 'INSERT INTO centers (name, location, capacity) VALUES (%s, %s, %s)'
  cursor.execute(query, (name, location, capacity))
  conn.commit()

def get_dosage(conn, center_id):
  cursor = conn.cursor()
  query = 'SELECT date, SUM(dosage) FROM dosages WHERE center_id = %s GROUP BY date'
  cursor.execute(query, (center_id,))
  dosages = cursor.fetchall()
  return dosages

def main(conn, args):
  if args['action'] == 'login':
    role = login(conn, args['username'], args['password'])
    if role:
      print(f'Logged in as {role}')
    else:
      print('Invalid username or password')
  elif args['action'] == 'signup':
    signup(conn, args['username'], args['password'], args['role'])
    print('User created successfully')
  elif args['action'] == 'search':
    centers = search_centers(conn, args['location'])
    print(f'Centers in {args['location']}:')
    for center in centers:
      print(center)
  elif args['action'] == 'apply':
    result = apply_vaccination(conn, args['center_id'])
    if result:
      print('Vaccination applied successfully')
    else:
      print('All slots are full')
  elif args['action'] == 'add':
    add_center(conn, args['name'], args['location'], args['capacity'])
    print('Vaccination center added successfully')
  elif args['action'] == 'get':
    dosages = get_dosage(conn, args['center_id'])
    print(f'Dosage details for center {args['center_id']}:')
    for date, dosage in dosages:
      print(f'{date}: {dosage}')


if __name__ == '__main__':
  args = parse_args()
  conn = mysql.connector.connect(
    host='localhost',
    user='user',
    password='',
    database='covid_vaccination'
  )
  try:
    main(conn, args)
  finally:
    conn.close()

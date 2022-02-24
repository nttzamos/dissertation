from models.profile import get_profile_id
from shared.database_handler import connect_to_database

def create_student(name, profiles):
  con, cur = connect_to_database()

  cur.execute('INSERT INTO student VALUES (null, ?)', (name,))
  con.commit()
  con.close()

  add_student_profiles(cur.lastrowid, profiles)

def update_student_name(student_id, new_student_name):
  con, cur = connect_to_database()

  cur.execute('UPDATE student SET name = ? WHERE id = ?', (new_student_name, student_id))
  con.commit()
  con.close()

def destroy_student(id):
  con, cur = connect_to_database()

  cur.execute('DELETE FROM student WHERE id = ?', (id,))
  cur.execute('DELETE FROM student_profile WHERE student_id = ?', (id,))
  con.commit()
  con.close()

def get_students():
  con, cur = connect_to_database()
  cur.execute('SELECT name FROM student ORDER BY name')
  students = list(map(lambda student: student[0], cur.fetchall()))

  con.close()
  return students

def get_student_details(student_name):
  con, cur = connect_to_database()
  cur.execute('SELECT id FROM student WHERE name = ?', (student_name,))
  student_id = cur.fetchone()[0]
  con.close()
  return student_id, get_student_profiles(student_id)

def student_name_exists(student_name):
  con, cur = connect_to_database()
  cur.execute('SELECT COUNT(*) FROM student WHERE name = ?', (student_name,))
  student_name_exists = cur.fetchone()[0] > 0
  con.close()

  return student_name_exists

def add_student_profiles(student_id, profiles):
  con, cur = connect_to_database()
  for profile in profiles:
    profile_id = get_profile_id(profile)
    cur.execute('INSERT INTO student_profile VALUES (null, ?, ?)', (student_id, profile_id))

  con.commit()
  con.close()

def remove_student_profiles(student_id, profiles):
  con, cur = connect_to_database()

  for profile in profiles:
    profile_id = get_profile_id(profile)
    cur.execute('DELETE FROM student_profile WHERE student_id = ? AND profile_id = ?', (student_id, profile_id))

  con.commit()
  con.close()

def get_student_profiles(student_id):
  con, cur = connect_to_database()

  query = ('SELECT name FROM profile '
    'INNER JOIN student_profile ON profile.id = student_profile.profile_id '
    'WHERE student_profile.student_id = ? ORDER BY name')

  cur.execute(query, (student_id,))
  profile_names = list(map(lambda profile_name: profile_name[0], cur.fetchall()))

  con.close()

  return profile_names

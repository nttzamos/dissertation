from shared.database_handler import get_grades, get_grade_subjects, connect_to_database
from models.subject import get_subject_id

def create_default_grade_profiles():
  grade_names = get_grades()
  for grade in range(1, 7):
    grade_subjects = get_grade_subjects(grade)
    create_profile(grade_names[grade - 1], grade, grade_subjects)

def create_profile(name, grade, subjects):
  con, cur = connect_to_database()
  cur.execute('SELECT name, id FROM subject WHERE grade_id = ?', (grade,))
  subject_dictionary = dict(cur.fetchall())

  subject_ids = []
  for subject in subjects:
    subject_ids.append(subject_dictionary[subject])

  cur.execute('INSERT INTO profile VALUES (null, ?, ?)', (name, grade))
  profile_subjects = list(zip([cur.lastrowid] * len(subject_ids), subject_ids))
  cur.executemany('INSERT INTO profile_subject VALUES (null, ?, ?)', profile_subjects)

  con.commit()
  con.close()

def update_profile_name(profile_id, new_profile_name):
  con, cur = connect_to_database()
  cur.execute('UPDATE profile SET name = ? WHERE id = ?', (new_profile_name, profile_id))

  con.commit()
  con.close()

def destroy_profile(id):
  con, cur = connect_to_database()
  cur.execute('DELETE FROM profile WHERE id = ?', (id,))
  cur.execute('DELETE FROM profile_subject WHERE profile_id = ?', (id,))
  cur.execute('DELETE FROM student_profile WHERE profile_id = ?', (id,))

  con.commit()
  con.close()

def get_profiles():
  con, cur = connect_to_database()
  cur.execute('SELECT name FROM profile ORDER BY name')
  profiles = list(map(lambda profile: profile[0], cur.fetchall()))

  con.close()
  return profiles

def get_profile_id(profile_name):
  con, cur = connect_to_database()
  cur.execute('SELECT id FROM profile WHERE name = ?', (profile_name,))
  profile_id = cur.fetchone()[0]
  con.close()

  return profile_id

def get_profile_name(profile_id):
  con, cur = connect_to_database()
  cur.execute('SELECT name FROM profile WHERE id = ?', (profile_id,))
  profile_name = cur.fetchone()[0]
  con.close()

  return profile_name

def get_profile_details(profile_name):
  con, cur = connect_to_database()
  cur.execute('SELECT id, grade_id FROM profile WHERE name = ?', (profile_name,))
  profile_id, grade_id = cur.fetchone()

  cur.execute('SELECT name FROM grade WHERE id = ?', (grade_id,))
  grade_name = cur.fetchone()[0]

  query = ('SELECT name '
    'FROM subject INNER JOIN profile_subject ON subject.id = profile_subject.subject_id '
    'WHERE profile_subject.profile_id = ? ORDER BY name')

  cur.execute(query, (profile_id,))
  profile_subjects = list(map(lambda word: word[0], cur.fetchall()))

  con.close()
  return profile_id, grade_id, grade_name, profile_subjects

def profile_name_exists(profile_name):
  con, cur = connect_to_database()
  cur.execute('SELECT COUNT(*) FROM profile WHERE name = ?', (profile_name,))
  profile_name_exists = cur.fetchone()[0] > 0
  con.close()

  return profile_name_exists

def add_profile_subjects(grade_id, profile_id, subjects):
  con, cur = connect_to_database()

  subjects_ids = []
  for subject in subjects:
    subjects_ids.append(get_subject_id(grade_id, subject))

  profile_subjects = list(zip([profile_id] * len(subjects_ids), subjects_ids))
  cur.executemany('INSERT INTO profile_subject VALUES (null, ?, ?)', profile_subjects)

  con.commit()
  con.close()

def remove_profile_subjects(grade_id, profile_id, subjects):
  con, cur = connect_to_database()

  for subject in subjects:
    query = 'DELETE FROM profile_subject WHERE profile_id = ? AND subject_id = ?'
    cur.execute(query, (profile_id, get_subject_id(grade_id, subject)))

  con.commit()
  con.close()

def get_profile_subject_ids(profile_id):
  con, cur = connect_to_database()
  cur.execute('SELECT subject_id FROM profile_subject WHERE profile_id = ?', (profile_id,))

  profile_subjects = list(map(lambda subject: subject[0], cur.fetchall()))

  con.close()
  return profile_subjects

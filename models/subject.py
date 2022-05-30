from shared.database_handler import connect_to_database

def get_subject_id(grade_id, subject):
  con, cur = connect_to_database()

  query = 'SELECT id FROM subject WHERE grade_id = ? AND name = ?'
  cur.execute(query, (grade_id, subject))
  subject_id = cur.fetchone()[0]
  con.close()

  return subject_id

def get_subject_name(subject_id):
  con, cur = connect_to_database()
  cur.execute('SELECT name FROM subject WHERE id = ?', (subject_id,))
  subject_name = cur.fetchone()[0]
  con.close()

  return subject_name

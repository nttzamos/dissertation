from shared.database_handler import connect_to_database

con, cur = connect_to_database()

cur.execute('CREATE INDEX profile_id_index ON profile (id)')
cur.execute('CREATE INDEX profile_name_index ON profile (name)')
cur.execute('CREATE INDEX non_related_word_index ON non_related_word (word_id_1, word_id_2)')
cur.execute('CREATE INDEX word_grade_id_index ON word (grade_id)')
cur.execute('CREATE INDEX word_grade_id_word_index ON word (word, grade_id)')
cur.execute('CREATE INDEX subject_word_index ON subject_word (word_id, subject_id)')

con.commit()
con.close()

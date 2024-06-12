import sqlalchemy as db

# Establish connection to PostgreSQL
engine = db.create_engine('postgresql://user:password@localhost/enrollmentdb')
connection = engine.connect()
metadata = db.MetaData()

# Create courses table
courses = db.Table('courses', metadata,
                   db.Column('id', db.Integer(), primary_key=True),
                   db.Column('title', db.String(255), nullable=False),
                   db.Column('description', db.String(255), nullable=False),
                   db.Column('credits', db.Integer())
                  )

# Create students table
students = db.Table('students', metadata,
                    db.Column('id', db.Integer(), primary_key=True),
                    db.Column('name', db.String(255), nullable=False),
                    db.Column('enrolled_courses', db.ARRAY(db.Integer))
                   )

metadata.create_all(engine)  # Creates the table

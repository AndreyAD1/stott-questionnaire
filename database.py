from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///questionnaire.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Child(Base):
    __tablename__ = 'respondents'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    sex = Column(String(10))
    grade_number = Column(Integer)

    def __init__(self, age, sex, grade_number):
        self.age = age
        self.sex = sex
        self.grade_number = grade_number

    def __repr__(self):
        return '<Child id={} age={} sex={} grade_number={}>'.format(
            self.id,
            self.age,
            self.sex,
            self.grade_number
        )


def create_database():
    Base.metadata.create_all(engine)


def add_person_to_database(age, sex, grade_number):
    child = Child(age=age, sex=sex, grade_number=grade_number)
    session.add(child)
    return


def add_behavioral_disorder_symptoms():
    pass


def add_person_aptitudes():
    pass


if __name__ == '__main__':
    create_database()

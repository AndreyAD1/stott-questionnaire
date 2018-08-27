from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///questionnaire.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    person_info = relationship('PersonInfo')

    def __repr__(self):
        return '<Person id={}>'.format(self.id)


class PersonInfo(Base):
    __tablename__ = 'person_info'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    sex = Column(String(10))
    grade_number = Column(Integer)
    person_id = Column(Integer, ForeignKey('person.id'))

    def __init__(self, personal_id, age, sex, grade_number):
        self.person_id = personal_id
        self.age = age
        self.sex = sex
        self.grade_number = grade_number

    def __repr__(self):
        return '<Person_info id={} age={} sex={} grade_number={}>'.format(
            self.person_id,
            self.age,
            self.sex,
            self.grade_number
        )


# class BehaviourSymptom(Base):
#


def create_database():
    Base.metadata.create_all(engine)


def add_person_to_database(age, sex, grade_number):
    person = Person()
    session.add(person)
    session.commit()
    person_info = PersonInfo(
        personal_id=person.id,
        age=age,
        sex=sex,
        grade_number=grade_number
    )
    session.add(person_info)
    print(session.query(PersonInfo).all())
    print(person, person.person_info)
    return


def add_behavioral_disorder_symptoms():
    pass


def add_person_aptitudes():
    pass


if __name__ == '__main__':
    create_database()

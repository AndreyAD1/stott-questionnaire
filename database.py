from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///questionnaire.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    person_info = relationship('PersonInfo', back_populates="person")

    def __repr__(self):
        return '<Person id={}>'.format(self.id)


class PersonInfo(Base):
    __tablename__ = 'person_info'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    age = Column(Integer)
    sex = Column(String(10))
    grade_number = Column(Integer)

    person = relationship('Person', back_populates='person_info')
    symptoms = relationship(
        'Symptoms',
        uselist=False,
        back_populates="person_info"
    )

    def __repr__(self):
        return '<Person_info id={} age={} sex={} grade_number={}>'.format(
            self.person_id,
            self.age,
            self.sex,
            self.grade_number
        )


class Symptoms(Base):
    __tablename__ = 'symptoms'
    id = Column(Integer, primary_key=True)
    person_info_id = Column(Integer, ForeignKey('person_info.id'))

    person_info = relationship('PersonInfo', back_populates='symptoms')

    symptom_1_1_1_1 = Column(Boolean())
    symptom_1_1_1_2 = Column(Boolean())
    symptom_1_1_1_3 = Column(Boolean())
    symptom_1_1_1_4 = Column(Boolean())
    symptom_1_1_1_5 = Column(Boolean())
    symptom_1_1_1_6 = Column(Boolean())
    symptom_1_1_1_7 = Column(Boolean())
    symptom_1_1_1_8 = Column(Boolean())
    symptom_1_1_1_9 = Column(Boolean())
    symptom_1_1_1_10 = Column(Boolean())

    symptom_1_1_2_1 = Column(Boolean())
    symptom_1_1_2_2 = Column(Boolean())
    symptom_1_1_2_3 = Column(Boolean())
    symptom_1_1_2_4 = Column(Boolean())
    symptom_1_1_2_5 = Column(Boolean())
    symptom_1_1_2_6 = Column(Boolean())
    symptom_1_1_2_7 = Column(Boolean())


def create_database():
    Base.metadata.create_all(engine)


def add_person_to_database(age, sex, grade_number):
    person = Person()
    session.add(person)
    session.commit()
    person_info = PersonInfo(
        person_id=person.id,
        age=age,
        sex=sex,
        grade_number=grade_number
    )
    session.add(person_info)
    print(session.query(PersonInfo).all())
    session.commit()
    return person.id


def add_behavioral_disorder_symptoms(
    person_info_id,
    input_symptoms
):
    symptoms_list = Symptoms.__table__.columns.keys()
    matched_symptoms = {}
    for symptom_name in input_symptoms.keys():
        if symptom_name in symptoms_list:
            matched_symptoms[symptom_name] = True

    symptoms = Symptoms(
        person_info_id=person_info_id,
        **matched_symptoms
    )
    print(symptoms)
    # session.add(symptoms)
    # # session.commit()
    #
    # print(session.query(Symptoms).all())

    return


def add_person_aptitudes():
    pass


if __name__ == '__main__':
    create_database()

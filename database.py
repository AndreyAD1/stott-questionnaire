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

    def __repr__(self):
        return '<Person_info id={} age={} sex={} grade_number={}>'.format(
            self.person_id,
            self.age,
            self.sex,
            self.grade_number
        )


class SymptomsOfAnxietyAboutAdults(Base):
    __tablename__ = 'anxiety_about_adults'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    symptom_1 = Column(String(200))
    symptom_2 = Column(String(200))
    symptom_3 = Column(String(200))
    symptom_4 = Column(String(200))
    symptom_5 = Column(String(200))
    symptom_6 = Column(String(200))
    symptom_7 = Column(String(200))


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
    # print(person, person.person_info)
    return person.id


def add_behavioral_disorder_symptoms(
    person_id,
    input_data,
    symptom_1=None,
    symptom_2=None,
    symptom_3=None,
    symptom_4=None,
    symptom_5=None,
    symptom_6=None,
    symptom_7=None
):
    for symptom_name in input_data.keys():
        print(symptom_name)
    # symptoms_of_anxiety_about_adults = SymptomsOfAnxietyAboutAdults(
    #     person_id=person.id,
    #     symptom_1=symptom_1,
    #     symptom_2=symptom_2,
    #     symptom_3=symptom_3,
    #     symptom_4=symptom_4,
    #     symptom_5=symptom_5,
    #     symptom_6=symptom_6,
    #     symptom_7=symptom_7
    # )
    # session.add(symptoms_of_anxiety_about_adults)
    # print(session.query(SymptomsOfAnxietyAboutAdults).all())

    print(person_id)
    return


def add_person_aptitudes():
    pass


if __name__ == '__main__':
    create_database()

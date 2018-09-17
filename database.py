from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


application = Flask(__name__)
application.config[
    'SQLALCHEMY_DATABASE_URI'
] = 'postgresql://stott:stott@localhost/stott_questionnaire'
application.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(application)


class Person(db.Model):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    person_info = relationship('PersonInfo', back_populates="person")

    def __repr__(self):
        return '<Person id={}>'.format(self.id)


class PersonInfo(db.Model):
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
    aptitudes = relationship(
        'Aptitudes',
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


class Symptoms(db.Model):
    __tablename__ = 'symptoms'
    id = Column(Integer, primary_key=True)
    person_info_id = Column(Integer, ForeignKey('person_info.id'))
    symptoms = Column(postgresql.ARRAY(String))
    person_info = relationship('PersonInfo', back_populates='symptoms')

    def __repr__(self):
        return '<Symptoms person_info_id={} person_info={} symptoms={}>'.format(
            self.person_info_id,
            self.person_info,
            self.symptoms
        )


class Aptitudes(db.Model):
    __tablename__ = 'aptitudes'
    id = Column(Integer, primary_key=True)
    person_info_id = Column(Integer, ForeignKey('person_info.id'))
    aptitudes = Column(postgresql.ARRAY(String))
    person_info = relationship('PersonInfo', back_populates='aptitudes')

    def __repr__(self):
        return '<Aptitudes person_info_id={} person_info={} aptitudes={}>'.format(
            self.person_info_id,
            self.person_info,
            self.aptitudes
        )


def create_database():
    db.create_all()


def add_person_to_database(age, sex, grade_number):
    person = Person()
    db.session.add(person)
    db.session.commit()
    person_info = PersonInfo(
        person_id=person.id,
        age=age,
        sex=sex,
        grade_number=grade_number
    )
    db.session.add(person_info)
    db.session.commit()
    return person_info.id


def add_symptoms_to_database(person_info_id, symptom_list):
    symptoms = Symptoms(person_info_id=person_info_id, symptoms=symptom_list)
    db.session.add(symptoms)
    db.session.commit()
    return


def add_aptitudes_to_database(person_info_id, aptitude_list):
    aptitudes = Aptitudes(person_info_id=person_info_id, aptitudes=aptitude_list)
    db.session.add(aptitudes)
    db.session.commit()
    return


if __name__ == '__main__':
    create_database()

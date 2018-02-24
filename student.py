#!/usr/bin/env python3
import csv
import sys

class Student:
    roster = []  #list of not matched student
    tandems = []
    languages = set()

    def __init__(self, row):
        self.name = row[1].strip()
        self.surname = row[2].strip()
        self.email = row[3].strip()
        self.nationality = row[4].strip()
        self.known_lang = row[5]
        self.wanted_lang = row[6]
        self.age = row[7].strip()
        self.gender = row[8].strip()
        self.university = row[9].strip()
        self.avail = row[10]

        self.partner = None

        self._roster_uptodate = False
        self._viable_tandems = None

        # remove duplicate
        exist = False
        for other in Student.roster:
            if not exist and (self.name.lower() == other.name.lower() and self.surname.lower() == other.surname.lower()) or self.email.lower() == other.email.lower():
                print(other)
                print(self)
                ans = input('Est-ce que ce sont les mêmes personnes ? [O/n] ')
                if ans.lower() == 'n':
                    print('Réponse prise en compte. Ce sont deux participants différents.\n')
                else:
                    print('Copie effacé !\n')
                    exist = True
            if not exist: other._roster_uptodate = False
        if not exist:
            Student.roster.append(self)
            for lang in self.list_known + self.list_wanted:
                Student.languages.add(lang)

    @property
    def list_known(self):
        return [lang.strip() for lang in self.known_lang.split(',')]

    @property
    def list_wanted(self):
        return [lang.strip() for lang in self.wanted_lang.split(',')]

    @property
    def viable_tandems(self):
        if self._roster_uptodate:
            return self._viable_tandems

        self._roster_uptodate = True
        self._viable_tandems = []
        for other in Student.roster:
            if id(other) != id(self) and\
                    set(other.list_known).intersection(self.list_wanted) and\
                    set(other.list_wanted).intersection(self.list_known):
                self._viable_tandems.append(other)
        return self._viable_tandems

    @property
    def gen_email(self):
        if self.partner:
            return '''************************************************************************************************
************************************************************************************************

mail à envoyer à {0.surname} {0.name} : {0.email}


Bonjour {0.surname},
L'association IntEGre te contacte suite à ton inscription à notre programme Tandem.

Nous avons le plaisir de t'annoncer qu'un tandem t'a été attribué : {1.surname} {1.name}
Ses langues parlées couramment sont : {1.known_lang}.

Voici son adresse mail, tu peux dès à présent le contacter : {1.email}
Néanmoins si tu rencontres le moindre problème n'hésite pas à nous recontacter.

Vous pouvez vous donner rendez-vous de façon hebdomadaire et dès le Lundi 29 janvier 2018 à partir de 18h00 à EVE au cours de nos Cafés-Tandem !
Tu peux retrouver toutes les informations sur l'événement en cliquant sur le lien suivant : http://bit.ly/LAssociationIntEGre

Merci d'accuser réception de ce message.
Cordialement,

-------------------------------------------------------------------------------------------------------------------------

Hi {0.surname}
IntEGre is contacting you about your subscription to our Tandem program.

We are pleased to inform you that a tandem is now assigned to you : {1.surname} {1.name} , whose languages fluently spoken are : {1.known_lang}
Here is his email: {1.email}
However if you have any problem you can contact us.

You can meet your tandem every week on Mondays, starting January 29, 2018, from 6pm at EVE during our Cafes-Tandem events !
You can find all the information about the event clicking on the following link : http://bit.ly/LAssociationIntEGre

Kind regards

L'Association IntEGre.

'''.format(self, self.partner)
        else:
            return '''************************************************************************************************
************************************************************************************************

mail à envoyer à {0.surname} {0.name} : {0.email}


Bonjour {0.surname},

L'association IntEGre te contacte suite à ton inscription à notre programme de tandem.

Nous sommes désolés de t'annoncer que nous n’avons pas pu t’attribuer de tandem pour le moment.
Cependant, nous vous gardons dans le programme dans l'espoir qu'un profil compatible s'inscrive prochainement.

D'ici là, nous te donnons rendez vous dès le Lundi 29 janvier 2018 à partir de 18h00 à EVE pour nos Cafés-Tandem hebdomadaires ! Tu auras l’occasion de rencontrer d’autres personnes dans ton cas et pourquoi pas un futur tandem !
Tu peux retrouver toutes les informations sur l'événement en cliquant sur le lien suivant : http://bit.ly/LAssociationIntEGre

En espérant que tu trouves un tandem bientôt,

Cordialement,

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Hi {0.surname},
IntEGre is contacting you about your subscription to our Tandem program.

We are sorry to inform you that we haven’t been able to assign a tandem to you yet.
However, we keep you in our Tandem program until we find a matching profile, hopefully very soon.

Meanwhile, we invite you to join us on Mondays, starting January 29, 2018, from 6.00pm at EVE for our weekly Cafes-Tandem events, where you will meet other students in your situation, and maybe find a tandem there !
You can find all the information about the event clicking on the following link : http://bit.ly/LAssociationIntEGre

Kind regards

L'Association IntEGre

'''.format(self)

    def __str__(self):
        """define str(student), e.g. print(student)"""
        return 'Nom: {name} Prenom: {surname} Addresse Mail: {email} Nation: {nationality} Langues connues: {known_lang} Langues cherchées: {wanted_lang} Age: {age} Sexe: {gender} Universite: {university} Date de première disponibilité: {avail}'.format_map(self.__dict__)


    def pair_with(self, other):
        for student in Student.roster:
            student._roster_uptodate = False
        if not self.partner and other in Student.roster:
            Student.tandems.append((self, other))
            self.partner = other
            other.partner = self
            Student.roster.remove(self)
            Student.roster.remove(other)


    @classmethod
    def load(cls, filename, legacy=False):
        """load a csv into a list of students"""
        with open(filename) as f:
            reader = csv.reader(f)
            if not legacy:  # discard the first line
                next(reader)
            for row in reader:
                cls(row)

    @classmethod
    def to_str(cls):
        strs = []
        for student in sorted(cls.roster, key=lambda x: x.name.lower()):
            strs.append(str(student))
        return '\r\n\r\n'.join(strs)


if __name__ == '__main__':
    legacy = False
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == '-l' or sys.argv[1].lower() == '--legacy':
            legacy = True



    with open('log.txt', 'w') as log:

        Student.load(input('Quel est le nom du fichier à charger ? '), legacy)
        print(Student.to_str(), file=log)

        print('Il y a {} langues en total.'.format(len(Student.languages)))
        print('', file=log)
        for lang in Student.languages:
            print(lang, file=log)

        nb_stud = len(Student.roster)

        for s in sorted(Student.roster, key=lambda x: len(x.viable_tandems)):
            if not s.partner and s.viable_tandems:
                s.pair_with(s.viable_tandems[0])

        print('{} tandems et {} étudiants seuls (sur {}).'.format(len(Student.tandems), len(Student.roster), nb_stud))

        print("\n{} éudiants n'ont pas de tandem :".format(len(Student.roster)), file=log)

        with open('email.txt', 'w') as email:
            for alone in Student.roster:
                print(alone.gen_email, file=email)
                print(alone.surname, alone.name, file=log)

            for tandem in Student.tandems:
                print(tandem[0].gen_email, file=email)
                print(tandem[1].gen_email, file=email)

    input()

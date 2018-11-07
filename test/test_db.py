import models
import db


it_project = models.Project(name='IT')
financial_project = models.Project(name='Financial')
db.session.add(it_project)
db.session.add(financial_project)

cathy = models.User(name='Cathy')
marry = models.User(name='Marry')
john = models.User(name='John')
db.session.add(cathy)
db.session.add(marry)
db.session.add(john)

cathy.projects.append(financial_project)
marry.projects.append(financial_project)
john.projects.append(it_project)
john.projects.append(financial_project)

db.session.commit()
#db.session.close()

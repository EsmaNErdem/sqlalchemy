from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()
# if table isn't empy, empty it
User.query.delete()

# # create new users
mike = User(first_name='Mike', last_name='Baker', image_url='https://capitolmuseum.ca.gov/wp-content/uploads/AnimalIMAGE-min.jpg')
esma = User(first_name='Esma', last_name='Erdem', image_url='https://hips.hearstapps.com/hmg-prod/images/dog-jokes-1581711487.jpg?crop=0.684xw:1.00xh;0.274xw,0&resize=1200:*')
smokey = User(first_name='Smokey', last_name='Kittiler', image_url='https://thumbs.dreamstime.com/b/funny-close-up-portrait-tabby-maine-coon-cat-194565488.jpg')

# # add them to session
db.session.add(mike)
db.session.add(esma)
db.session.add(smokey)

# # commit 
db.session.commit()
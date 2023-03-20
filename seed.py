from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()
# if table isn't empy, empty it
User.query.delete()
Post.query.delete()

# # create new users
mike = User(first_name='Mike', last_name='Baker', image_url='https://i.pinimg.com/736x/1b/9a/26/1b9a26a9093f63773bd7c2d54f26bbd2--funny-stuff-google-search.jpg')
esma = User(first_name='Esma', last_name='Erdem', image_url='https://hips.hearstapps.com/hmg-prod/images/dog-jokes-1581711487.jpg?crop=0.684xw:1.00xh;0.274xw,0&resize=1200:*')
smokey = User(first_name='Smokey', last_name='Kittiler', image_url='https://thumbs.dreamstime.com/b/funny-close-up-portrait-tabby-maine-coon-cat-194565488.jpg')

# # add them to session and commit
db.session.add(mike)
db.session.add(esma)
db.session.add(smokey)
db.session.commit()

post1 = Post(title='First', content='Am I a spoiled first?', user_id=1)
post2 = Post(title='Second', content='Am I a fun second?', user_id=1)
post3 = Post(title='Third', content='Am I a turd third?', user_id=1)

db.session.add_all([post1, post2, post3])
db.session.commit()


tag1 = Tag(name="Fun")
tag2 = Tag(name="Even More")
tag3 = Tag(name="Bloop")

db.session.add_all([tag1, tag2, tag3])
db.session.commit()

post_tag1 = PostTag(post_id=1, tag_id=1)
post_tag2 = PostTag(post_id=1, tag_id=2)
post_tag3 = PostTag(post_id=1, tag_id=3)
post_tag4 = PostTag(post_id=2, tag_id=1)
post_tag5 = PostTag(post_id=3, tag_id=1)

db.session.add_all([post_tag1, post_tag2, post_tag3, post_tag4, post_tag5])
db.session.commit()
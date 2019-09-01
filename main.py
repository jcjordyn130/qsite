import qsite

qsite.base.metadata.create_all(qsite.engine)
session = qsite.newsession()

# Make a new user.
u = qsite.User()
u.name = "John B Doe P.H.D"
u.description = "Just an average Joe with a doctorate in whatever the I want."
session.add(u)
session.commit()

# Make another user.
utwo = qsite.User()
utwo.name = "Some Random User"
utwo.descirption = " I am just a random userrssfgdfdf"
session.add(utwo)
session.commit()
session.flush()

# Make a follow.
follow = qsite.Follow()
follower = u.id
followee = utwo.id
session.add(follow)
session.commit()

# Make a new question.
q = qsite.Question()
q.title = "How much RAM is in a Raspberry Pi 3"
q.details = "A Raspberry Pi 2 is acceptable as well. \n Thanks!"

print(q)

session.add(q)
session.commit()
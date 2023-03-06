     
def add_user_in_database(database, user_class)-> None:
    """add a user with all of it's infos, name, email, etc... in our database"""
    database.session.add(user_class)
    database.session.commit()

def get_user(database_modal, email):
    """keep hold of a user, knowing the email"""
    return database_modal.query.filter_by(email= email).first()

def update_score(database, new_score, user):
    """updating our user score"""
    user.highest_score = new_score
    database.session.commit()
    
     
    
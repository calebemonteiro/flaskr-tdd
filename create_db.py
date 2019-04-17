from app import db
from models import Flaskr
# 
# Create the database and tables
db.create_all()
#
# Commit changes
db.session.commit()
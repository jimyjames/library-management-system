from library import db
from flask import current_app



class CrudOps:

    def add(self, data):
        db.session.add(data)

        return db.session.commit
    
    def update(self):
        return db.session.commit
    
    def delete(self,data):
        db.session.delete(data)
        return db.session.commit        
    

class Members(CrudOps,db.Model):
    __tablename__="members"
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(30),nullable=False)
    middle_name=db.Column(db.String(30),nullable=False)
    last_name=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(30),nullable=False)
    phone=db.Column(db.String(30),nullable=False)
    gender=db.Column(db.String(30),nullable=False)
    created_at=db.Column(db.DateTime(),default=db.func.current_timestamp())
    borrower=db.relationship("Borrowed",backref="borrower",lazy=True)



class Books(CrudOps,db.Model):
    __tablename__="books"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(30),unique=True, nullable=False)
    author=db.Column(db.String(30),nullable=False)
    created_at=db.Column(db.DateTime(),default=db.func.current_timestamp()) 
    quantity=db.Column(db.Integer(),nullable=False)
    available=db.Column(db.Integer(),nullable=False)
    books_borrowed=db.relationship("Borrowed",backref="books_borrowed",lazy=True)


class Borrowed(CrudOps,db.Model):
    __tablename__="borrowed"
    id=db.Column(db.Integer,primary_key=True)
    member_id=db.Column(db.Integer(),db.ForeignKey("members.id"),nullable=False)
    book_id=db.Column(db.Integer(),db.ForeignKey("books.id"),nullable=False)
    issued_at=db.Column(db.DateTime(),default=db.func.current_timestamp())
    expected_at=db.Column(db.DateTime(),default=db.func.current_timestamp())
    returned_at=db.Column(db.DateTime(),default=db.func.current_timestamp())
    fine=db.Column(db.Integer())
    status=db.Column(db.String(30),nullable=False)

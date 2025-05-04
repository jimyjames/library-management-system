from library import db,create_app
from library.models import Books, Members, Borrowed
import json
# from flask_cors import CORS

app = create_app("default")
# CORS(app)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Books": Books, "Members": Members, "Borrowed": Borrowed}

@app.cli.command("create_db")
def create_db():
    """Create the database."""
    db.create_all()
    print("Database created successfully!")
@app.cli.command("drop_db")
def drop_db():
    """Drop the database."""
    db.drop_all()
    print("Database dropped successfully!")
@app.cli.command("seed_db")    
def seed_db():  
    """Seed the database with initial data."""
    with open("library/seed_data.json") as f:
        data = json.load(f)
        for model, records in data.items():
            for record in records:
                if model == "Books":
                    book = Books(**record)
                    db.session.add(book)
                elif model == "Members":
                    member = Members(**record)
                    db.session.add(member)
                elif model == "Borrowed":
                    borrowed = Borrowed(**record)
                    db.session.add(borrowed)
        db.session.commit()
    print("Database seeded successfully!")
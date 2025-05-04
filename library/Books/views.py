from library.Books import books
from library.models import CrudOps,Books
from flask import render_template, redirect, url_for, flash, request,jsonify
from library.schemas import  BooksIn, BooksOut
from pydantic import ValidationError
from library import db




@books.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method =='POST':
        try:
            book=BooksIn(**request.json)
            
               
            if book==None:
                return jsonify({"error":"book values { title,author,quantity,available} is required"}), 400

            new_book= Books(
                title=book.title,
                author=book.author,
                quantity=book.quantity,
                available=book.available
            )
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('books.add_book'))
        except ValidationError as e:
            return jsonify({"errors":e.errors()}), 400
       
     
    
    allbooks = Books.query.all()
    return jsonify([BooksOut.from_orm(book).model_dump() for book in allbooks]), 200

@books.route('/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Books.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

@books.route('/update/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        edit_book = BooksIn(**request.json) 
        book = Books.query.get_or_404(book_id)
        book.title = edit_book.title
        book.author = edit_book.author
        book.quantity = edit_book
        book.available = edit_book.available
        db.session.commit()
        return jsonify({"message": "Book updated successfully"}), 200
    except ValidationError as e:
        return jsonify({"errors":e.errors()}), 400  

@books.route('/list', methods=['GET'])
def list_books():
    if request.method == 'GET':
               return("this is the books template")

    # books = Books.query.all()
    # return jsonify ([BooksOut.from_orm(books).dict() for books in books ]), 201


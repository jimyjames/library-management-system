from library.Books import books
from library.models import CrudOps,Books
from flask import render_template, redirect, url_for, flash, request,jsonify
from library.schemas import  BooksIn, BooksOut
from pydantic import ValidationError
from library import db
from flask_cors import cross_origin




@books.route('/add', methods=['GET', 'POST'])
@cross_origin()
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
@cross_origin()
def delete_book(book_id):
    book = Books.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

@books.route('/update/<int:book_id>', methods=['PUT'])
@cross_origin()
def update_book(book_id):
    try:
        edit_book = BooksIn(**request.json) 
        print("edit_book",edit_book)
        book = Books.query.get_or_404(book_id)
        book.title = edit_book.title
        book.author = edit_book.author
        book.quantity = edit_book.quantity
        book.available = edit_book.available
        db.session.commit()
        return jsonify({"message": "Book updated successfully"}), 200
    except ValidationError as e:
        return jsonify({"errors":e.errors()}), 400  



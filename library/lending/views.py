from library.lending import lending
from library import db
from flask import request, jsonify, flash, redirect, url_for
from library.models import Borrowed, Books, Members
from library.schemas import BorrowedIn, BorrowedOut
from pydantic import ValidationError
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import aliased
from flask_cors import cross_origin



@lending.route('/add', methods=['POST', 'GET'])
@cross_origin()
def add_lending():
    if request.method == 'POST':
        try:
            new_lending = BorrowedIn(**request.json)
            book_id = new_lending.book_id
            member_id = new_lending.member_id
            issued_at = datetime.now()
            expected_at = new_lending.expected_at
            book = Books.query.filter_by(id=book_id).first()

            member = Members.query.filter_by(id=member_id).first()
            if expected_at is None:
                expected_at = datetime.now() + timedelta(days=14)
            if book is None or member is None:
                return jsonify({"error": "Book or member not found"}), 404
            if book.available == 0:
                return jsonify({"error": "Book not available"}), 400
            if expected_at < issued_at: 
                return jsonify({"error": "Expected return date must be after issue date"}), 400
            if expected_at > issued_at + timedelta(days=32):
                return jsonify({"error": "Expected return date cannot be more than 30 days from issue date"}), 400
            
            lending = Borrowed(
                member_id=member_id,
                book_id=book_id,
                issued_at=issued_at,
                expected_at=expected_at,
                returned_at=None,
                status='active'
            )
            db.session.add(lending)
            book.available -= 1
            db.session.commit()
            return jsonify({"message": "Lending added successfully"}), 201
        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    all_lendings = Borrowed.query.all()
    book_alias = aliased(Books)
    member_alias = aliased(Members)
    lendings = Borrowed.query.options(db.joinedload(Borrowed.books_borrowed), db.joinedload(Borrowed.borrower)).all()

    

    return jsonify([BorrowedOut.from_orm(lending).dict() for lending in lendings]), 200
@lending.route('/<int:lending_id>', methods=['GET'])
@cross_origin()
def get_lending(lending_id):
    lending = Borrowed.query.get(lending_id)
    if lending is None:
        return jsonify({"error": "Lending not found"}), 404
    return jsonify(BorrowedOut.from_orm(lending).dict()), 200
@lending.route('/<int:lending_id>', methods=['PUT'])
@cross_origin()
def update_lending(lending_id):
    try:
        lending = Borrowed.query.get(lending_id)
        if lending is None:
            return jsonify({"error": "Lending not found"}), 404
        updated_lending = BorrowedIn(**request.json)
        book_id = updated_lending.book_id
        member_id = updated_lending.member_id
        book = Books.query.filter_by(id=book_id).first()
        member = Members.query.filter_by(id=member_id).first()
        if book is None or member is None:
            return jsonify({"error": "Book or member not found"}), 404
        if updated_lending.expected_at < lending.issued_at: 
            return jsonify({"error": "Expected return date must be after issue date"}), 400
        if updated_lending.expected_at > lending.issued_at + timedelta(days=30):
            return jsonify({"error": "Expected return date cannot be more than 30 days from issue date"}), 400
        
        lending.book_id = book_id
        lending.member_id = member_id
        # lending.issued_at = datetime.now() | updated_lending.issued_at if updated_lending.issued_at else lending.issued_at
        lending.expected_at = updated_lending.expected_at
        db.session.commit()
        return jsonify(BorrowedOut.from_orm(lending).dict()), 200
        # return jsonify({"message": "Lending updated successfully"}), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
@lending.route('/<int:lending_id>', methods=['DELETE'])
@cross_origin()
def delete_lending(lending_id):    
    lending = Borrowed.query.get(lending_id)
    if lending is None:
        return jsonify({"error": "Lending not found"}), 404
    if lending.status == 'returned':
        return jsonify({"error": "Lending already returned"}), 400
    book = Books.query.filter_by(id=lending.book_id).first()
    book.available += 1
    db.session.delete(lending)
    db.session.commit()
    return jsonify({"message": "Lending deleted successfully"}), 200


@lending.route('/<int:lending_id>/return', methods=['PUT'])
@cross_origin()
def return_lending(lending_id):
    try:
        lending = Borrowed.query.get(lending_id)
        if lending is None:
            return jsonify({"error": "Lending not found"}), 404
        if lending.status == 'returned':
            return jsonify({"error": "Lending already returned"}), 400
        book = Books.query.filter_by(id=lending.book_id).first()
        if book is None:
            return jsonify({"error": "Book not found"}), 404
        # Calculate fine if any
        fine = 0
        if lending.expected_at < datetime.now():
            days_overdue = (datetime.now() - lending.expected_at).days
            fine = days_overdue * 50  # Assuming a fine of $5 per day
        lending.returned_at = datetime.now()
        lending.status = 'returned'
        lending.fine = fine if fine < 501 else 500
        book.available += 1
        db.session.commit()
        return jsonify(BorrowedOut.from_orm(lending).dict()), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
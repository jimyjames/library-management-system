from library.members import members
from flask import render_template, request, redirect, url_for, flash,jsonify
from library.models import Members, Borrowed, Books
from library.schemas import  MembersIn, MembersOut
from library import db
from pydantic import ValidationError


@members.route('/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        try:
            member = MembersIn(**request.json)
            
            if member is None:
                return jsonify({"error": "member values { name, email, phone } is required"}), 400
            
            email_exists = Members.query.filter_by(email=member.email).first()
            if email_exists:
                return jsonify({"error": "Email already exists"}), 400
            phone_exists = Members.query.filter_by(phone=member.phone).first()
            if phone_exists:
                return jsonify({"error": "Phone number already exists"}), 400

            new_member = Members(
                first_name=member.first_name,
                middle_name=member.middle_name,
                last_name=member.last_name,
                email=member.email,
                phone=member.phone,
                gender=member.gender
            )
            db.session.add(new_member)
            db.session.commit()
            flash('Member added successfully!', 'success')
            return redirect(url_for('members.add_member'))
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 400

    all_members = Members.query.all()
    return jsonify([MembersOut.from_orm(member).model_dump() for member in all_members]), 200

@members.route('/delete/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = Members.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted successfully"}), 200

@members.route('/update/<int:member_id>', methods=['PUT'])
def update_member(member_id):    
    try:
        edit_member = MembersIn(**request.json) 
        member = Members.query.get_or_404(member_id)
        member.first_name = edit_member.first_name
        member.middle_name = edit_member.middle_name
        member.last_name = edit_member.last_name
        member.email = edit_member.email
        member.phone = edit_member.phone
        member.gender = edit_member.gender
        db.session.commit()
        return jsonify({"message": "Member updated successfully"}), 200
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

# routes.py
from flask import render_template, request, session, redirect, url_for, flash ,  jsonify
from app import app
from user.models import User, Conversation, Message
import loadmodel

# Simple response model
def generate_response(user_input):
    # This is a simple example response, you can replace it with your actual response model
    return f"Thanks for your message: {user_input}. This is an entrepreneurial chatbot focused on providing business advice and support."

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone_number']
        email = request.form['email']

        if User.find_by_email(email):
            flash('Email already exists!')
            return render_template('register.html')
        else:
            user = User(username, password, phone_number, email)
            user.save()
            session['user_id'] = user.id
            # Create a new conversation for the user
            conversation = Conversation(title="Default Conversation", user_id=user.id)
            conversation.save()
            return redirect(url_for('chat', conversation_id=conversation.id))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = User.find_by_email(email)
        session.permanent = True
        if user_data:
            if password == user_data.password:
                session['user_id'] = user_data.id
                conversation = Conversation(title="Default Conversation", user_id=user_data.id)
                conversation.save()
                return redirect(url_for('chat', conversation_id=conversation.id))
            else:
                flash("Invalid password!")
                return render_template('login.html')
        else:
            flash("Email does not exist!")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/chat/<conversation_id>', methods=['GET', 'POST'])
def chat(conversation_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conversation = Conversation.find_by_id(conversation_id)
    if not conversation:
        flash("Conversation not found!")
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        user_input = request.form['message']
        response = generate_response(user_input)
        # Save user message
        user_message = Message(session['user_id'], conversation_id, user_input, True)
        user_message.save()
        # Save chatbot response
        bot_message = Message(session['user_id'], conversation_id, response, False)
        bot_message.save()

    messages = Message.find_by_conversation_id(conversation_id)
    return redirect(url_for('chat', conversation_id=conversation.id))


@app.route('/new_conversation', methods=['POST'])
def new_conversation():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.find_by_id(user_id)
        if user:
            conversation = Conversation(title="title", user_id=user.id)
            conversation.save()
            return redirect(url_for('chat', conversation_id=conversation.id))
    return jsonify({'error': 'User not logged in or invalid request'}), 400



@app.route('/generate_response', methods=['POST'])
def generate_response_route():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.find_by_id(user_id)
        if user:
            user_input = request.form['user_input']
            conversation_id = request.form['conversation_id']
            conversation = Conversation.find_by_id(conversation_id)
            if conversation and conversation.user_id == user_id:
                # Save the user's message
                message = Message(user_id, conversation_id, user_input, True)
                message.save()
                # Generate bot response
                bot_response = generate_response(user_input)
                # Save the bot's response
                bot_message = Message(user_id, conversation_id, bot_response, False)
                bot_message.save()
                return jsonify({'message': bot_response})
    return jsonify({'message': 'User not logged in or conversation not found'}), 400



@app.route('/delete_conversation/<conversation_id>', methods=['POST'])
def delete_conversation(conversation_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.find_by_id(user_id)
        conversation = Conversation.find_by_id(conversation_id)
        if user and conversation and conversation.user_id == user_id:
            conversation.delete()
            return jsonify({'success': True})
    return jsonify({'success': False}), 400

@app.route('/delete_message/<message_id>', methods=['POST'])
def delete_message(message_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.find_by_id(user_id)
        message = Message.find_by_id(message_id)
        if user and message and message.user_id == user_id:
            message.delete()
            return jsonify({'success': True})
    return jsonify({'success': False}), 400




@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))



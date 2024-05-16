from flask import render_template, request, session, redirect, url_for, flash
from app import app
from user.models import User, Conversation


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
        
        if User.find_by_username(username):
            flash('Email already exists!')
            return render_template('register.html')
        else:
            user = User(username, password, phone_number, email)
            user.save()
            session['username'] = user.username
            return redirect(url_for('chat'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user_data = User.find_by_email(email)
        
        if user_data:
            if password == user_data.password:
                session['username'] = user_data.username
                return redirect(url_for('chat'))
            else:
                flash("Invalid password!")
                return render_template('login.html')
        else:
            flash("Email does not exist!")
            return render_template('login.html')

    return render_template('login.html')


#@app.route('/chat', methods=['GET', 'POST'])
#def chat():
    #if 'username' in session:
        #username = session['username']
        #conversations = Conversation.find_by_user(username)
        #if request.method == 'POST':
        #   partner_username = 'chatbot'
        #    title = request.form['title']
        #    message = request.form['message']
        #    conversation = [(username, message)]

            # Preprocess the message for the model
        #    preprocessed_message = preprocess_message(message)

            # Generate chatbot response using your pre-trained model
        #    chatbot_response = generate_response(model, preprocessed_message)

        #    conversation.append(('chatbot', chatbot_response))
        #    new_conversation = Conversation(username, partner_username, title, conversation)
        #    new_conversation.save()

         #   return redirect(url_for('chat'))
       # return render_template('chat.html', username=username, conversations=conversations)
    #else:
     #   return redirect(url_for('login'))
@app.route('/chat')
def chat():
    if 'username' in session:
        username = session['username']
        conversations = Conversation.find_by_user(username)
        return render_template('chat.html', username=username, conversations=conversations)
    else:
        return redirect(url_for('login'))

@app.route('/new_conversation', methods=['POST'])
def new_conversation():
    if 'username' in session:
        username = session['username']
        new_conversation = Conversation(username, "chatbot", "Nouvelle conversation", [])
        new_conversation.save()
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))




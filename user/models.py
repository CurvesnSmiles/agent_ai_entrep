
from pymongo import MongoClient
import uuid
from datetime import datetime

client = MongoClient('localhost:27017')
db = client['chat_db']
users_collection = db['users']
conversations_collection = db['conversations']
messages_collection = db['messages']

class User:
    def __init__(self, username, password, phone_number, email, user_id=None):
        self.id = user_id if user_id else str(uuid.uuid4())
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.email = email

    def save(self):
        users_collection.insert_one(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'phone_number': self.phone_number,
            'email': self.email
        }
        
    def get_id(self):
        return self.id

    @staticmethod
    def find_by_id(user_id):
        user_data = users_collection.find_one({'id': user_id})
        if user_data:
            return User(
                user_data.get('username'),
                user_data.get('password'),
                user_data.get('phone_number'),
                user_data.get('email'),
                user_data.get('id')
            )
        return None

    @staticmethod
    def find_by_username(username):
        user_data = users_collection.find_one({'username': username})
        if user_data:
            return User(
                user_data.get('username'),
                user_data.get('password'),
                user_data.get('phone_number'),
                user_data.get('email'),
                user_data.get('id')
            )
        return None

    @staticmethod
    def find_by_email(email):
        user_data = users_collection.find_one({'email': email})
        if user_data:
            return User(
                user_data.get('username'),
                user_data.get('password'),
                user_data.get('phone_number'),
                user_data.get('email'),
                user_data.get('id')
            )
        return None

class Conversation:
    def __init__(self, title, user_id, conversation_id=None, date=None):
        self.id = conversation_id if conversation_id else str(uuid.uuid4())
        self.title = title
        self.user_id = user_id
        self.date = date if date else datetime.utcnow()

    def save(self):
        conversations_collection.insert_one(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id,
            'date': self.date
        }

    def update_title(self, new_title):
        conversations_collection.update_one(
            {'id': self.id},
            {'$set': {'title': new_title}}
        )
        self.title = new_title

    @staticmethod
    def find_by_id(conversation_id):
        conv_data = conversations_collection.find_one({'id': conversation_id})
        if conv_data:
            return Conversation(
                conv_data.get('title'),
                conv_data.get('user_id'),
                conv_data.get('id'),
                conv_data.get('date')
            )
        return None

    @staticmethod
    def find_by_user_id(user_id):
        conv_data = conversations_collection.find({'user_id': user_id})
        conversations = []
        for data in conv_data:
            conversations.append(Conversation(
                data.get('title'),
                data.get('user_id'),
                data.get('id'),
                data.get('date')
            ))
        return conversations

    def delete(self):
        conversations_collection.delete_one({'id': self.id})
        messages_collection.delete_many({'conversation_id': self.id})

class Message:
    def __init__(self, user_id, conversation_id, content, is_user_message, message_id=None):
        self.id = message_id if message_id else str(uuid.uuid4())
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.content = content
        self.is_user_message = is_user_message

    def save(self):
        messages_collection.insert_one(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'conversation_id': self.conversation_id,
            'content': self.content,
            'is_user_message': self.is_user_message
        }

    @staticmethod
    def find_by_conversation_id(conversation_id):
        messages_data = messages_collection.find({'conversation_id': conversation_id})
        messages = []
        for data in messages_data:
            messages.append(Message(
                data.get('user_id'),
                data.get('conversation_id'),
                data.get('content'),
                data.get('is_user_message'),
                data.get('id')
            ))
        return messages

    @staticmethod
    def find_by_id(message_id):
        message_data = messages_collection.find_one({'id': message_id})
        if message_data:
            return Message(
                message_data.get('user_id'),
                message_data.get('conversation_id'),
                message_data.get('content'),
                message_data.get('is_user_message'),
                message_data.get('id')
            )
        return None

    def delete(self):
        messages_collection.delete_one({'id': self.id})

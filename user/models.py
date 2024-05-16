from pymongo import MongoClient
import uuid


client = MongoClient('localhost:27017')
db = client['chat_db']
users_collection = db['users']
conversations_collection = db['conversations']

class User:
    def __init__(self, username, password, phone_number, email):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.email = email

  
    def save(self):
        users_collection.insert_one(self.to_dict())

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'phone_number': self.phone_number,
            'email': self.email
        }

    @staticmethod
    def find_by_username(username):
        user_data = users_collection.find_one({'username': username})
        if user_data:
            return User(
                user_data['username'],
                user_data['password'],
                user_data['phone_number'],
                user_data['email']
            )
        return None

    @staticmethod
    def find_by_phone_number(phone_number):
        user_data = users_collection.find_one({'phone_number': phone_number})
        if user_data:
            return User(
                user_data['username'],
                user_data['password'],
                user_data['phone_number'],
                user_data['email']
            )
        return None

    @staticmethod
    def find_by_email(email):
        user_data = users_collection.find_one({'email': email})
        print (user_data)
        if user_data:
            return User(
                user_data['username'],
                user_data['password'],
                user_data['phone_number'],
                user_data['email']
            )
        return None



class Conversation:
    def __init__(self, username, partner_username, title, conversation):
        self._id = str(uuid.uuid4())
        self.username = username
        self.partner_username = partner_username
        self.title = title
        self.conversation = conversation

    def save(self):
        conversations_collection.insert_one(self.to_dict())

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'partner_username': self.partner_username,
            'title': self.title,
            'conversation': self.conversation
        }

    @staticmethod
    def find_by_user(username):
        conversations_data = conversations_collection.find({'username': username})
        conversations = []
        for conv_data in conversations_data:
            conversations.append(Conversation(
                conv_data['username'],
                conv_data['partner_username'],
                conv_data['title'],
                conv_data['conversation']
            ))
        return conversations

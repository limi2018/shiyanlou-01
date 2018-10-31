from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/news'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
mongo = MongoClient('127.0.0.1', 27017).shiyanlou

from sqlalchemy import Column,String,Integer 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('File')
    
    def __init__(self, name):
        self.name = name


class File(db.Model):
    __tablename__ = 'File'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    create_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'))
    category = db.relationship('Category', uselist=False)
    content = db.Column(db.Text)
    
    def __init__(self, title, create_time, category, content):
        self.title = title
        self.create_time = create_time
        self.category = category
        self.content = content

    def add_tag(self, tag_name):
        file_item = mongo.File.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            if tag_name not in tags:
                tags.append(tag_name)
            mongo.File.update_one({'file_id': self.id}, {'$set': {'tags': tags}})

        else:
            tags = [tag_name]
            mongo.File.insert_one({'file_id': self.id, 'tags': tags})
        return tags

    def remove_tag(self, tag_name):
        file_item = mongo.File.find_one({'file_id': self.id}) 
        if file_item:
            tags = file_item['tags']
            try:
                tags.remove(tag_name) 
                new_tags = tags
            except ValueError:
                return tags
            mongo.File.update_one({'file_id': self.id}, {'$set': {'tags': new_tags}})
            return new_tags
        return []


    @property
    def tags(self):
        file_item = mongo.File.find_one({'file_id': self.id})
        if file_item:
            return file_item['tags']
        else:
            return []

def insert_datas():
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')

    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')

@app.route('/')
def index():
    return render_template('index.html', files=File.query.all())

@app.route('/files/<file_id>')
def file(file_id):
    f = File.query.get_or_404(file_id)
    return render_template('file.html', file=f)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
    

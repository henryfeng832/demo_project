from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app)

# 数据库配置
engine = create_engine('mysql+pymysql://root:t7d4j8m9@dbconn.sealoshzh.site:36452/demo_project_preview')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 用户模型
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)

# 创建表
Base.metadata.create_all(engine)

# API路由
@app.route('/api/users', methods=['GET'])
def get_users():
    session = Session()
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page
    
    users = session.query(User).offset(offset).limit(per_page).all()
    total = session.query(User).count()
    
    return jsonify({
        'users': [{'id': user.id, 'name': user.name, 'gender': user.gender} for user in users],
        'total': total
    })

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    session = Session()
    
    user = User(name=data['name'], gender=data['gender'])
    session.add(user)
    session.commit()
    
    return jsonify({'id': user.id, 'name': user.name, 'gender': user.gender})

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    session = Session()
    
    user = session.query(User).get(user_id)
    if user:
        user.name = data['name']
        user.gender = data['gender']
        session.commit()
        return jsonify({'id': user.id, 'name': user.name, 'gender': user.gender})
    
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
from flask import Flask, request, render_template
from flask_restful import Resource, Api
import dataset
import base64
import json
from flask_jsonpify import jsonify

db_connect = dataset.connect('sqlite:///data.db')
app = Flask(__name__)
api = Api(app)
db = 'labyrinth'

class Student(Resource):
    def __init__(self, instance_name, instance_domain):
        table = db_connect[db] 
        self.instance_name = instance_name
        self.instance_domain = instance_domain
        self.magic_key = self._get_magic_key(self.instance_name, self.instance_domain)
        self.step = 0
        self.points = 0

    def _get_magic_key(self, ins_name, ins_domain):
        s = ins_name + ins_domain
        return base64.b64encode(s.encode('utf-8'))

    def save(self):
        table = db_connect.get_table(db)
        db_entry = {}
        db_entry['i_name'] = self.instance_name 
        db_entry['i_domain'] = self.instance_domain
        db_entry['i_magic_key'] = self.magic_key 
        db_entry['step'] = self.step 
        db_entry['points'] = self.points
        print(type(db_entry))
        table.insert(db_entry)


class Register(Resource):
    def put(self):
        jsonData = request.get_json()
        instance_name = jsonData['i_name']
        instance_domain = jsonData['i_domain']
        if instance_name is '' and instance_domain is '':
            abort(400)
        new_student = Student(instance_name, instance_domain)
        new_student.save()


class Scoreboard(Resource):
    def get(self):
        result = []
        table = db_connect.get_table(db)
        students_data = table.all()
        for row in students_data:
            result.append(dict(row))

        return render_template('scoreboard.html', score=result)
       
#        return students_data
        
api.add_resource(Scoreboard, '/', '/scoreboard/')
api.add_resource(Register, '/register')
#api.add_resource(Students, '/students')


if __name__ == '__main__':
     app.run(debug=True)

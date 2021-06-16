from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testpassword@localhost/testdb'
db = SQLAlchemy(app)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key= True, nullable=False)
    team_name = db.Column(db.String(50), nullable=False)
    role = db.relationship('Role', backref='team')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String(50), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)


@app.route('/create-team', methods=['POST'])
def create_team():
    try:
        json_data = request.get_json()
        team_name = json_data['team_name']
        role_name = json_data['role_name']
        team = Team.query.filter_by(team_name=team_name).first()
        if team is None:
            team_obj = Team(team_name=team_name)
            db.session.add(team_obj)
            db.session.commit()

            role_obj = Role(role_name=role_name, team=team_obj)
            db.session.add(role_obj)
            db.session.commit()

            return jsonify({"message": "Team {0} with Role {1} is successfully created".format(team_name, role_name)}),201
        else:
            role = Role.query.filter_by(role_name=role_name).first()
            if role is None:
                role_obj = Role(role_name=role_name, team=team)
                db.session.add(role_obj)
                db.session.commit()
                return jsonify({"message": "Team {0} with Role {1} is successfully created".format(team_name, role_name)}),201
            return jsonify({"message": "Team {0} and Role {1} already exists".format(team_name, role_name)})
    except Exception as e:
        return jsonify({"message": "Something went wrong."}),500


@app.route('/get-roles/', methods=['GET'])
def get_roles():
    try:
        team_name = request.args.get('team_name', 'NA')
        if team_name != 'NA':
            team = Team.query.filter_by(team_name= team_name).first()
            if team is not None:
                all_roles = Role.query.filter_by(team_id=team.id).all()
                res_list = list()
                for role in all_roles:
                    role_name = role.role_name
                    res_list.append(
                        {"team_name": team_name,
                         "role_name": role_name})
                return jsonify({'details': res_list})
            else:
                return jsonify({'message': 'team {0} not found !!!'.format(team_name)})
        else:
            return jsonify({'message': 'Invalid query string !!!'})
    except Exception as e:
        print(e)
        return jsonify({'message': "Something went wrong."}),500


if __name__ == '__main__':
    app.run()

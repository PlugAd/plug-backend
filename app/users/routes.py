from app.users import user_bp
from flask_jwt_extended import jwt_required
from flask import render_template, request, jsonify
from app.users.schema import UserSchema

@user_bp.route('/')
def index():
    return render_template("index.html")

@user_bp.get("/all")
@jwt_required()
def get_all_users():
    from app.models.userAuthModel import User

    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)


    users = User.query.paginate(
        page=page,
        per_page=per_page
    )

    result = UserSchema().dump(users, many=True)

    return jsonify({
        "users":result
    }), 200
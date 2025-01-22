from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256 as sha256

# create Blueprint
todo_bp = Blueprint("todo", __name__, template_folder="../templates")


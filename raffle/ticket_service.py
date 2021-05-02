from flask import Blueprint, request, g
from raffle.db import get_db

# setting up blueprint for logical grouping
bp = Blueprint('ticket', __name__, url_prefix='/ticket')

# This function take care of providing tickets 
@bp.route('/<username>')
def get_ticket(username):
    return username
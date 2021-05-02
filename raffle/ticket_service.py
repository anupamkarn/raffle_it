from flask import Blueprint, request, g
from pymongo import ReturnDocument
from raffle.db import get_db
from bson import json_util
from datetime import datetime, timedelta
import random

# setting up blueprint for logical grouping
bp = Blueprint('ticket', __name__, url_prefix='/ticket')

"""
This method handles ticket distribution machanism. It works on the
basis of eventID. We have considered few decicion pointers such as
1) Ticket must be distributed on the basis of event. A Ticket belongs to a specific event.
2) User should not be allowed to take part twice in event life cycle
"""
@bp.route('/<username>')
def get_ticket(username):

    db = get_db()
    # when not passed, it will raise a bad request error
    event_id = request.args['eventID']
    # getting event related all details 
    event_record = db.events.find_one({'event_id': event_id}, { '_id': 0 })
    if event_record is None:
        return "No event exists with provided event id."
    
    elif len(event_record['ticket_list']) == 0:
        return "Unfortunately all tickets are distributed, try new Lucky draw event or wait for winner anoucement"
    
    elif any(participant['name'] == username for participant in event_record['participants']):
        return "You have already have ticket for this event."

    else:
        # ticket no. allocation logic resides here, we are maintaining a list of shuffled ticket numbers
        # along with all other details of event. To avoid any kind of collision we are popping out 
        # ticket and assigning it to users and storing it with event's details in  "participants"
        # property. 
        ticket_no = event_record['ticket_list'].pop()
        updated_record = db.events.find_one_and_update(
            {
                'event_id': event_id
            },
            {
                '$push': {'participants': {
                    'name': username,
                    'ticket_no': ticket_no 
                }},
                '$pop': {
                    'ticket_list': 1
                }
            },
            return_document=ReturnDocument.AFTER
        )
        
        return json_util.dumps(updated_record)

@bp.route('/upcoming')
def get_upcoming_draws():
    """
    This method returns list of draws which are comming up along with their rewards
    """
    db = get_db()
    start_time = datetime.now()
    end_time = start_time + timedelta(weeks=1)
    # querying the database to get list of all the lucky draw event which are 
    # to take place with in a span of a week. We are specifically checking draw_time
    # property of events objects.
    list_of_draws = db.events.find({'draw_time':{
        '$gte': start_time,
        '$lt': end_time
    }},{
        '_id': 1
    })

    return json_util.dumps(list_of_draws)

@bp.route('/winners')
def get_winners():
    """
    This method provides a list of all winners of Lucky draw events within a week.
    """
    db = get_db()
    end_time = datetime.now()
    start_time = end_time - timedelta(weeks=1)
    winners_list = db.winners.find({'draw_time':{
        '$gte': start_time,
        '$lt': end_time
    }},{
        '_id': 1
    })

    return json_util.dumps(list_of_draws)

@bp.route('/update_events')
def check_draw():
    """
    This method checks event's draw_time and update winners collection with winners list.
    """
    database = db.get_db()
    start_time = datetime.now() - timedelta(seconds=60)
    end_time = datetime.now() + timedelta(seconds=60)
    event_list = database.events.find({'draw_time': {
        '$gte': start_time,
        '$lt': end_time
    }}, {
        '_id': 1
    })
    winner_list = []
    for event in event_list:
        winner_index = random.randrange(0,len(event['participants'])-1)
        winner_record = {}
        winner_record['name'] = event['participants'][winner_index]['name']
        winner_record['ticket_no'] = event['participants'][winner_index]['ticket_no']
        winner_record['event'] = event['name']
        winner_record['reward'] = event['reward']
        winner_list.append(winner_record)

        if event['frequency'] == 'D':
            next_draw_time = event['draw_time'] + timedelta(days=1)
        elif event['frequency'] == 'W':
            next_draw_time = event['draw_time'] + timedelta(weeks=1)
        else:
            next_draw_time = event['draw_time'] + timedelta(days=365)
            
        database.events.update({
            'event_id': event['event_id']
        },
        {
            'draw_time': next_draw_time
        })
    
    database.winners.insert_many(winner_list)


    
    


    
    
    




    
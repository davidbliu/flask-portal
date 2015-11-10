import config
from flask import Flask, Response
import json, sys
from sets import Set

def get_email_from_token(token):
    return token.decode('hex')


def get_position(email):
    return 'chair'

def get_response(obj):
    return Response(json.dumps(obj), mimetype='application/json')


""" Points and attendance """

def get_attendance_hash(event_members, event_hash):
    h = {};
    seen = Set([])
    for em in event_members:
        if em['member_email'] not in seen:
            h[em['member_email']]=[]
            seen.add(em['member_email'])
        h[em['member_email']].append(event_hash[em.event_id])
    return h

        
    

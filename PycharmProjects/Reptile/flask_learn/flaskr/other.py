import functools
from hashlib import md5
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,abort,jsonify,current_app,make_response,send_file
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.auth import logind_require,cached
from flaskr.db import get_db
from datetime import datetime, timedelta
import os,time
from werkzeug.utils import secure_filename
import math
# from flaskr import cache
import re
import redis
import svgwrite


bp = Blueprint('other', __name__, url_prefix='/other')

client = redis.Redis()


def write_text(file_name, pv):
    dwg = svgwrite.Drawing(file_name, (200, 50))
    paragraph = dwg.add(dwg.g(font_size=14))
    paragraph.add(dwg.text(f"当前访问量：{pv}", (10, 20)))
    dwg.save()

@bp.route('/pv/<user_id>')
def calc_pv(user_id):
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'static','svg/')
    pv = client.hincrby('pv_count', user_id, 1)
    file_name = path + f'{user_id}.svg'
    write_text(file_name, pv)
    response = make_response(file_name)
    return send_file(file_name)

@bp.route('/get/pv') 
def get_pv():
    user_id = request.args.get('userid')
    if user_id is None:
        return render_template('auth/page_not_found.html'), 404
    return render_template('other/test_pv.html',user_id=user_id)

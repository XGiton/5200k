# -*- coding: utf-8 -*-
from flask import Blueprint


api = Blueprint('api', __name__, template_folder='template')


USER_ERROR = 1000

import user

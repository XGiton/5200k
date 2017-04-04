# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify


api = Blueprint('api', __name__, template_folder='template')


@api.errorhandler(400)
def handler_400(e):
    return jsonify(stat=0, err=0, msg='Bad Request'), 400


@api.errorhandler(401)
def handler_401(e):
    return jsonify(stat=0, err=1, msg='Unauthorized'), 401


@api.errorhandler(403)
def handler_402(e):
    return jsonify(stat=0, err=2, msg='Forbidden'), 403


@api.errorhandler(404)
def handler_403(e):
    return jsonify(stat=0, err=3, msg='Not Found'), 404

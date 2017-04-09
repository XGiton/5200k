# -*- encoding: utf-8 -*-
from flask import request, jsonify, session, abort
from flask_login import current_user, login_required

from . import api
from logic.image import logic_get_image_upload_url


class Error(object):
    pass


@api.route('/image/upload-url', methods=['GET'])
@login_required
def get_image_upload_url():
    """
    ## 获取图片上传url

        GET '/api/image/upload-url'

    Params:

    Returns:

    Errors:
    """
    pass

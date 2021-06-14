from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import RegisterBot
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        groupid = request.form.get('groupid')
        moderators = request.form.get('moderators').split(sep=",")
        chanelSlack=request.form.get('chanelSlack')
        botslack=request.form.get('botSlack')

        print(chanelSlack[0])


        if len(groupid) < 15:
            flash('groupid  is too short!', category='error')
        elif type(moderators) != list:
            flash('moderators list not a  coma', category='error')
        elif chanelSlack[0]!='#':
            flash('chanelSlack start with #', category='error')

        else:
            new_note = RegisterBot(FB_id_groop=groupid,
                                   user_id=current_user.id,
                                   FB_access_token='EAAB49HwRvEMBAP3ZBN9e22ASneff82zNK7YuovaNO7l36dvCENpIKtNGPvZB0kU9Q144YAdDkHZAZAiABDt5rbjxcyQDSFsDXRiIcVpmZCCjJd7pHhxUJVCUQkOEZAw1IWPB13y5ZADwqWNDMY2Snqv2W8tFM57IMPw9e0F2oNBBMLnFi4fwlR1B3jGQGzOYfKdY9DAZAZAK81D3J8FYgNmZBCqPjSBga8L79hoZBoikLocUDLsck3EFtkp',
                                   creator_post_skip=moderators,
                                   chanelSlack=chanelSlack,
                                   api_bot_secret_Slack=botslack
                                   )
            db.session.add(new_note)
            db.session.commit()
            flash('bot added', category='success')

    return render_template("home.html", user=current_user)



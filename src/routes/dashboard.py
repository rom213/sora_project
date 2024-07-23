from flask import Blueprint, render_template, request, redirect,url_for

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('')
def dashboard():
    return render_template('dashboard/body/body.html')



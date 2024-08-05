from flask import Blueprint, render_template, request, redirect,url_for
from models.ModelSection import ModelSection
from models.ModelUser import ModelUser

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/allotment')
def dashboard():
    sections= ModelSection.allSections()
    users= ModelUser.allUsers()
    return render_template('dashboard/body/body.html', sections=sections,users=users)

@dashboard_bp.route('/users')
def usersdash():
    sections= ModelSection.allSections()
    users= ModelUser.allUsers()
    return render_template('dashboard/body/body.html', users=users,sections=sections)





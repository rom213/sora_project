from flask import Blueprint, render_template, request, redirect,url_for
from models.ModelSection import ModelSection

section_bp = Blueprint('sections', __name__)

@section_bp.route('/all')
def allslots():
    sections=ModelSection.allSections()
    return render_template('dashboard/body/body.html', sections=sections)



@section_bp.route('', methods=['GET', 'POST'])
def slot():
    if request.method=='POST':
        data=request.form['description']
        ModelSection.create(data)
        return redirect(url_for('dashboard.dashboard'))


from flask import Blueprint, render_template, request, redirect,url_for

slot_bp = Blueprint('slot', __name__)

@slot_bp.route('/all')
def allslots():
    return render_template('dashboard/body/body.html')

@slot_bp.route('', methods=['GET', 'POST'])
def slot():
    print('maria')
    if request.method=='POST':
        return redirect(url_for('dashboard.dashboard'))


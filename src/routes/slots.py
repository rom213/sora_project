from flask import Blueprint, render_template, request, redirect,url_for
from models.ModelSlot import ModelSlot

slot_bp = Blueprint('slots', __name__)

@slot_bp.route('/all')
def allslots():
    sections=ModelSlot.allSlots()
    return render_template('dashboard/body/body.html', sections=sections)

@slot_bp.route('', methods=['GET', 'POST'])
def slot():
    if request.method=='POST':
        section_id=request.form['section_id']
        ModelSlot.create(car_id=None,section_id=section_id)
        return redirect(url_for('dashboard.dashboard'))
    
@slot_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method=='POST':
        slot_id=request.form['slot_id']
        ModelSlot.delete(slot_id=slot_id)
        return redirect(url_for('dashboard.dashboard'))
    



from .entities.Conexion import Conexion
from .entities.User import User
from datetime import datetime
from sqlalchemy import asc, desc



from .entities.State import State
from sqlalchemy import or_, and_, func
from datetime import timedelta


from flask_login import current_user

from . import db


class ModelState:
    @classmethod
    def create(cls, path_img,title,):
        try:
            user_id = current_user.id

            state = State(image=path_img, title=title, user_id=user_id)
            
            db.session.add(state)
            db.session.commit()
            
            return
            
        except Exception as e:
            raise e
        
    @classmethod
    def allStates(cls, user_log):
        try:
            conexions = Conexion.query.with_entities(Conexion.user_id, Conexion.user_id2).filter(
                and_(
                    or_(
                        Conexion.user_id == user_log, 
                        Conexion.user_id2 == user_log
                    ), 
                    Conexion.conexion_type == 'toato',
                    Conexion.delete_at == None
                )
            ).order_by(asc(Conexion.id)).all()
            
            user_id_list=[]
            user_id_list.append(user_log)
            for conexion in conexions:
                user_id, user_id2 = conexion
                if user_id != user_log:
                    user_id_list.append(user_id)
                if user_id2 != user_log:
                    user_id_list.append(user_id2)
      

            states_for_user=[]




            for id in user_id_list:
                states_tem = State.query.filter(
                    State.user_id == id,
                    and_(
                        State.delete_at.is_(None)
                    )
                ).order_by(desc(State.id)).all()


                states=[]
                user = User.query.filter(User.id == id).first()
                states.append(
                    {
                        'id': user.id,
                        'avatar':user.avatar,
                        "fullname":user.name + ' ' + user.lastname,
                        "letters":user.init_letters(),
                        "color": user.color,
                    }
                )


                st=[]
                for state in states_tem:
                    if datetime.utcnow()-state.created_at < timedelta(hours=12):
                        st.append(
                            {
                                'imagen':state.image,
                                'title':state.title
                                
                            }
                        )
                states.append(st)
                if st:
                    states_for_user.append(states)
            

            return states_for_user



            

                
            
                            

            
        except Exception as e:
            raise e

# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def get_login():
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Max-Age"] = 86400
    response.headers["Access-Control-Allow-Headers"] = '*'
    response.headers["Access-Control-Allow-Methods"] = '*'
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    global usuario
    usuario=request.get_vars['usuario']
    password = request.get_vars['clave']
    if db((db.Usuarios.nombre_user == usuario) & (db.Usuarios.clave == password)).isempty():
        estado={'status': 0 , 'msj':'Contraseña o usuario incorrecto'}
    else:
        estado={'status': 1 , 'msj':'Usuario Logueado'}
    return response.json(estado)

def get_lista():
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Max-Age"] = 86400
    response.headers["Access-Control-Allow-Headers"] = '*'
    response.headers["Access-Control-Allow-Methods"] = '*'
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    tareas=db.executesql('Select id, descripcion, cerrada from Tareas order by ID;', as_dict=True)
    return response.json(tareas)

def set_tarea_cerrada():
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Max-Age"] = 86400
    response.headers["Access-Control-Allow-Headers"] = '*'
    response.headers["Access-Control-Allow-Methods"] = '*'
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    id_tarea = request.get_vars['id']
    esta_cerrada = request.get_vars['cerrar']
    if db((db.Tareas.id == id_tarea)).isempty():
        estado={'status': 0 , 'msj':'Error, la tarea ingresada no existe'}
    else:
        db(db.Tareas.id==id_tarea).update(cerrada=esta_cerrada)
        estado={'status': 1 , 'msj':'Cambio de Estado de Tarea Exitoso'}
    return response.json(estado)

def set_nueva_tarea():
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Max-Age"] = 86400
    response.headers["Access-Control-Allow-Headers"] = '*'
    response.headers["Access-Control-Allow-Methods"] = '*'
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    descripcion = request.get_vars['descripcion_tarea']
    cerrada = request.get_vars['estado']
    db.Tareas.insert(descripcion=descripcion, cerrada = cerrada, id_user=1)
    estado={'status': 1, 'msj': 'La Tarea fue agregada con éxito'}
    return response.json(estado)

def set_editar_tarea():
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Max-Age"] = 86400
    response.headers["Access-Control-Allow-Headers"] = '*'
    response.headers["Access-Control-Allow-Methods"] = '*'
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    id_tarea = request.get_vars['id']
    descripcion_tarea = request.get_vars['descripcion']
    if db((db.Tareas.id == id_tarea)).isempty():
        estado={'status': 0 , 'msj':'Error, la tarea ingresada no existe'}
    else:
        if not descripcion_tarea:
            estado={'status': 0, 'msj': 'Error, la descripcion no puede estar vacia'}
        else:
            db(db.Tareas.id==id_tarea).update(descripcion=descripcion_tarea)
            estado={'status': 1 , 'msj':'Descripcion modificada con éxito'}
    return response.json(estado)

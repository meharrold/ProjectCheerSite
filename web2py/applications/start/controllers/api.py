#import tempfile

# Cloud-safe of uuid, so that many cloned servers do not all use the same uuids.
#from gluon.utils import web2py_uuid

# Here go your api methods.


def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


@auth.requires_signature(hash_vars=False)
def get_images():
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    images = []
    has_more = False
    rows = db(db.user_images.user_email == auth.user.email).select(db.user_images.ALL, limitby=(start_idx, end_idx + 1), orderby=~db.user_images.id)

    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            m = dict(
                id = r.id,
                user_email = r.user_email,
                image_url = r.image_url
            )
            images.append(m)
        else:
            has_more = True
    logged_in = auth.user is not None
    return response.json(dict(images=images, looged_in=logged_in, has_more=has_more,))


def get_users():
    users = []
    if auth.user is not None:
        rows = db(db.auth_user.email != auth.user.email).select(db.auth_user.ALL)
    else:
        rows = db().select(db.auth_user.ALL)

    for i, r in enumerate(rows):
        m = dict(
            id=r.id,
            user_email=r.email,
            user_name=get_user_name_from_email(r.email)
        )
        users.append(m)

    return response.json(dict(users=users,))


def get_user_images():
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    user_email = request.vars.user_email if request.vars.user_email is not None else ""

    has_more = False
    images = []
    rows = db(db.user_images.user_email == user_email).select(db.user_images.ALL, limitby=(start_idx, end_idx + 1),  orderby=~db.user_images.id)

    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            m = dict(
                id = r.id,
                user_email = r.user_email,
                image_url = r.image_url
            )
            images.append(m)
        else:
            has_more = True
    logged_in = auth.user is not None
    return response.json(dict(images=images, looged_in=logged_in, has_more=has_more,))

@auth.requires_signature()
def add_image():
    m_id = db.user_images.insert(
        image_url = request.vars.image_url
    )
    m = db.user_images(m_id)
    image = dict(
        id = m.id,
        image_url = m.image_url
    )
    return response.json(dict(image=image))

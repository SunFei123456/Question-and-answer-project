from functools import wraps

from flask import redirect, g, url_for


def login_required(func):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """

    # 保留原来函数的信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))

    return inner


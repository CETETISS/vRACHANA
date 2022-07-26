from .base_imports import *

class NodeJSONEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, ObjectId):
      return str(o)

    if isinstance(o, datetime.datetime):
      return o.strftime("%d/%m/%Y %H:%M:%S:%f")

    return json.JSONEncoder.default(self, o)


class ActiveUsers(object):
    """docstring for ActiveUsers"""

    @staticmethod
    def get_active_id_session_keys():
        # Query all non-expired sessions
        # use timezone.now() instead of datetime.now() in latest versions of Django
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        # uid_list = []
        # uid_list_append = uid_list.append
        # session_key_list = []
        userid_session_key_dict = {}

        # Build a list of user ids from that query
        for session in sessions:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id', 0)
            if user_id:
                userid_session_key_dict[user_id] = session.session_key
            # uid_list_append(user_id)
            # session_key_list.append(session.session_key)

        return userid_session_key_dict

        # # Query all logged in users based on id list
        # if list_of_ids:
        #     return User.objects.filter(id__in=uid_list).values_list('id', flat=True)
        # else:
        #     return User.objects.filter(id__in=uid_list)

    @staticmethod
    def logout_all_users():
        """
        Read all available users and all available not expired sessions. Then
        logout from each session. This method also releases all buddies with each user session.
        """
        from django.utils.importlib import import_module
        from django.conf import settings
        from django.contrib.auth import logout
        from .buddy import Buddy
        
        request = HttpRequest()

        # sessions = Session.objects.filter(expire_date__gte=timezone.now())
        sessions = Session.objects.filter(expire_date__gte=timezone.now()).distinct('session_data')

        # Experimental trial (aggregate query):
        # unique_sessions_list = Session.objects.filter(expire_date__gte=timezone.now()).values('session_data').annotate(Count('session_data')).filter(session_data__count__lte=1)
        
        print('Found %d non-expired session(s).' % len(sessions))

        for session in sessions:
            try:
                user_id = session.get_decoded().get('_auth_user_id')
                engine = import_module(settings.SESSION_ENGINE)
                request.session = engine.SessionStore(session.session_key)

                request.user = User.objects.get(id=user_id)
                print ('\nProcessing session of [ %d : "%s" ]' % (request.user.id, request.user.username))

                logout(request)
                print('- Successfully logout user with id: %r ' % user_id)

            except Exception as e:
                # print "Exception: ", e
                pass

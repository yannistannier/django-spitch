

class AuthMeMixin(object):

    def get_object(self):
        return self.request.user
from kanpai import Kanpai


class AuthSchemas:

    @staticmethod
    def validateLogin(requestJson):
        schema = Kanpai.Object({
            'email': (Kanpai.Email(error="Invalid email provided")
                      .required(error='Please provide email.')
                      .max(256, error='Maximum allowed length is 256')),

            'password': (Kanpai.String(error='Must be string')
                         .required(error='Please provide user password.')
                         .max(256, error='Maximum allowed length is 256')
                         .match(r'^.{5,}$', 'Minimum allowed length is 5'))
        })

        return schema.validate(requestJson)

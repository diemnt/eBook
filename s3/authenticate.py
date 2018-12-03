import jwt
from jwt import exceptions
import datetime
from s3 import constants


# key = 'tiendangdht@gmail.com'
# encoded = jwt.encode({'path': 'book/The_Meg.mp4', 'exp': datetime.datetime.utcnow()}, key, algorithm='HS256')
# encoded = jwt.encode({'path': 'book/The_Meg.mp4'}, key, algorithm='HS256')
# 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
# jwt.decode(encoded, key, leeway=dt.timedelta(seconds=120), algorithms='HS256')

# {'some': 'payload'}

def setting(name, default=None):
    """
    Helper function to get a Django setting by name or (optionally) return
    a default (or else ``None``).
    """
    return getattr(constants, name, default)


class S3AuthenticateJWT(object):
    secret = setting("MEDIA_SECRET_KEY")
    time_leeway = setting("S3_JWT_LEEWAY", 120)
    algorithm = setting("SIGNATURE_ALGORITHMS", "HS256")

    def __init__(self):
        print "secret ",setting("MEDIA_SECRET_KEY")
        if not self.secret:
            raise Exception("Please provider MEDIA_SECRET_KEY")

    @classmethod
    def encoding(self, payload, is_verify_leeway=True):
        try:
            if is_verify_leeway:
                payload['exp'] = datetime.datetime.utcnow()
            encoded = jwt.encode(payload, self.secret, algorithm=self.algorithm)
            
            return encoded

        except Exception, e:
            return Exception("Cannot decoding payload")


    @classmethod
    def decoding(self, encoded, leeway=time_leeway, is_verify_leeway=True):
        try:
            print "#### Call method decoding ",is_verify_leeway
            if is_verify_leeway:
                print "using leeway"
                payload = jwt.decode(encoded, self.secret, leeway=datetime.timedelta(seconds=leeway), algorithms=self.algorithm)
                
            else:
                print "#### not using leeway"
                payload = jwt.decode(encoded, self.secret, algorithms=self.algorithm)
                
            
            return payload

        except exceptions.ExpiredSignatureError:
            return Exception("Signature has expired")
        except Exception, e:
            return Exception("Cannot decoding payload 11", e)



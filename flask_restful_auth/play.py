import uuid
import jwt
import datetime

# sha256('1')
key = '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b'

id = str(uuid.uuid4())
experation = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

packet = {
    'id': id,
    'exp': experation,
}

token = jwt.encode(packet, key, algorithm="HS256")

print('token', token)
print('decode', jwt.decode(token, key, "HS256"))
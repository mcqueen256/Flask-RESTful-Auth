from random import randint
ids = []

def checkid(id):
    '''Unique ID identification'''
    if id in ids:
        return True
    return False

class Group:
    '''Creating Group'''
    members = []
    def __init__(self,name):
        self.name = name
        temp_id = randint(1,10**2) #for 100users
        result = checkid(temp_id)
        if result:
            self.id = temp_id
            ids.append(self.id)
    
    def add_members(self,users: list):
        '''Add members to group'''
        for user in users:
            self.members.append(users.id)
    
    def leave(self,members: list):
        '''Kick members out of the group'''
        for user in members:
            members.remove(user)

class User:
    '''User Registration'''
    group = {}
    def __init__(self,name,password,username,email):
        self.name = name
        self.password = password
        self.username = username
        self.email = email
        temp_id = randint(1,10**2) #for 100users
        result = checkid(temp_id)
        if result:
            self.id = temp_id
            ids.append(self.id)

    def create_group(self,grp_name):
        '''User creating a group'''
        grp = Group(grp_name)
        self.group[grp.id] = (grp,True) # true is for grp admin  

    def add_grp_member(self,grp_id,members: list):
        '''Admn user Adding members to group'''
        if grp_id in self.group:
            if self.group[grp_id][1]:
                self.group[grp_id][0].add_members(members)
    
    def kick_out_members(self,grp_id,members: list):
        '''Admin User kicking member out of the Group'''
        if grp_id in self.group:
            if self.group[grp_id][1]:
                self.group[grp_id][0].leave(members)

    def change_admin(self,grp_id,members: list,add: bool,delete = False):
        '''Change group admin'''
        if grp_id in self.group:
            if self.group[grp_id][1]:
                if add:
                    for user in members:
                        user.group[grp_id] = (self.group[grp_id][0],True)
                elif delete:
                    for user in members:
                        user.group[grp_id] = (self.group[grp_id][0],False)
class UserDTO:
    def __init__(self, userId, username, chatID) -> None:
        self.userId = userId
        self.username = username
        self.chatID = chatID

    def to_dict(self):
        return {
            'userId': self.userId,
            'username': self.username,
            'chatID': self.chatID
        }
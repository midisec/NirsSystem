from wtforms import Form

class BaseForm(Form):
    def get_error(self):
        print(self.errors)
        # message = self.errors.popitem()[1][0]
        message = self.errors
        message = list(message.items())[0][1][0]
        return message

    def validate(self):
        return super(BaseForm, self).validate()
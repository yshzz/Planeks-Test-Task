class DefaultGroupNotFound(ValueError):
    def __init__(self, groupname):
        super().__init__(
            f'Default group "{groupname}" not found.\n'
            'Please run "create_default_groups" command with manage.py'
        )


class MailgunError(ValueError):
    pass

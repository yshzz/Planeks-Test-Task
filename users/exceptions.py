class DefaultGroupNotFound(ValueError):
    def __init__(self, groupname):
        super().__init__((
                'Default group "{0}" not found.\n'
                'Please run "create_default_groups" command with manage.py'
            ).format(groupname))

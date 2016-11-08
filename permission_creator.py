from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType


def add_permissions_group(group_name, permissions):
    """
    :param group_name: The name of the group to add the permissions to
    :param permissions: A list of tuples on the form (codename, name) each representing a single permission
    :return: None
    Creates or gets the group with the given name before adding permissions to the group
    """

    group, created = Group.objects.get_or_create(name=group_name)

    # Loop through each permission
    for codename, name in permissions:

        # Create the permission
        permission, created = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=ContentType.objects.get_or_create(app_label="band_booking", model="global_permission")[0]
        )

        # Add the permission to the group
        group.permissions.add(permission)


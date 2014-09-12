import sys
sys.path.append('/etc/sentry')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'conf'

USERNAME, PASSWORD, EMAIL = sys.argv[1:]

def main():
    # Bootstrap the Sentry environment
    from sentry.utils.runner import (
        configure_app,
        generate_settings,
        initialize_app,
    )

    configure_app(
        project='sentry',
        default_config_path='/etc/sentry/conf.py',
        default_settings='sentry.conf.server',
        settings_initializer=generate_settings,
        settings_envvar='SENTRY_CONF',
        initializer=initialize_app,
    )
    # Do something crazy
    from sentry.models import Team, Project, ProjectKey, User

    admin = User.objects.filter(username='admin')
    team = Team.objects.filter(name='OSF')

    if admin:
        admin = admin[0]
    else:
        admin = User()
        admin.username = 'admin'
        admin.email = 'admin@localhost'
        admin.is_superuser = True
        admin.set_password('admin')
        admin.save()

    if team:
        team = team[0]
    else:
        team = Team()
        team.name = 'OSF'
        team.owner = admin[0]
        team.save()


    osf_prod = Project.objects.filter(name='OSF Production')
    osf_staging = Project.objects.filter(name='OSF Staging')

    if not osf_prod:
        osf_prod = Project()
        osf_prod.team = team
        osf_prod.owner = admin
        osf_prod.name = 'OSF Production'
        osf_prod.save()

    if not osf_staging:
        osf_staging = Project()
        osf_staging.team = team
        osf_staging.owner = admin
        osf_staging.name = 'OSF Staging'
        osf_staging.save()

main()

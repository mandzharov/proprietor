# A Django test project

The idea of the site is to make a digital building management system.

## Test Data details

The password for all users: admin123123

User emails:

| email | account type |
| --- | --- |
| todor.zhivkov@bkp.com | superuser |
| jeffrey.dahmer@killer.com | manager |
| edmund.kemper@killer.com | manager |
| mikhail.popkov@killer.com | manager |
| katherine.knight@killer.com | manager |
| andrei.chikatilo@killer.com | user |

To load the data run:
```bash
python manage.py loaddata sample_data.json
```

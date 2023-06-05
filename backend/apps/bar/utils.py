from apps.bar.models import BarAccountLog


def add_account_change_log(action, value, account, user_id):
    return BarAccountLog.objects.create(bar_account=account, change_by_id=user_id, action=action, value=value)
from django.db import models

from djadmin.base.flow import Flow


class AccountTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    account_address = models.ForeignKey('Accounts', models.DO_NOTHING, db_column='account_address')
    token_name = models.TextField()
    token_address = models.TextField()
    token_type = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_tokens'
        unique_together = (('account_address', 'token_name', 'token_address'),)


class AccountsManager(models.Manager):
    flow = Flow()

    def add_on_flow(self):
        response = self.flow.post_new_account()
        return response

    def get_all_from_flow(self):
        response = self.flow.get_all_accounts()
        return response

    def get_one_from_flow(self, address: str):
        response = self.flow.get_account_by_address(address=address)
        return response


class Accounts(models.Model):
    objects = AccountsManager()

    address = models.TextField(primary_key=True)
    type = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts'
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class ChainEventsStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    latest_height = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chain_events_status'


class IdempotencyKeys(models.Model):
    key = models.TextField(primary_key=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'idempotency_keys'


class Jobs(models.Model):
    id = models.UUIDField(primary_key=True)
    error = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    transaction_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    exec_count = models.BigIntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    attributes = models.JSONField(blank=True, null=True)
    errors = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'jobs'
        verbose_name = "Job"
        verbose_name_plural = "Jobs"


class Migrations(models.Model):
    id = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'migrations'


class ProposalKeys(models.Model):
    id = models.BigAutoField(primary_key=True)
    key_index = models.BigIntegerField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proposal_keys'


class StorableKeys(models.Model):
    id = models.BigAutoField(primary_key=True)
    account_address = models.TextField(blank=True, null=True)
    index = models.BigIntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    value = models.BinaryField(blank=True, null=True)
    sign_algo = models.TextField(blank=True, null=True)
    hash_algo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    public_key = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'storable_keys'


class SystemSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    maintenance_mode = models.BooleanField(blank=True, null=True)
    paused_since = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_settings'


class TokenTransfers(models.Model):
    id = models.BigAutoField(primary_key=True)
    transaction_id = models.TextField(blank=True, null=True)
    recipient_address = models.TextField(blank=True, null=True)
    sender_address = models.TextField(blank=True, null=True)
    ft_amount = models.TextField(blank=True, null=True)
    nft_id = models.BigIntegerField(blank=True, null=True)
    token_name = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'token_transfers'


class Tokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(unique=True)
    name_lower_case = models.TextField(blank=True, null=True)
    address = models.TextField()
    setup = models.TextField(blank=True, null=True)
    transfer = models.TextField(blank=True, null=True)
    balance = models.TextField(blank=True, null=True)
    type = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokens'


class Transactions(models.Model):
    transaction_id = models.TextField(primary_key=True)
    transaction_type = models.BigIntegerField(blank=True, null=True)
    proposer_address = models.TextField(blank=True, null=True)
    flow_transaction = models.BinaryField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transactions'

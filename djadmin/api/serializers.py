from rest_framework import serializers


class KeySerializer(serializers.Serializer):
    index = serializers.IntegerField()
    type = serializers.CharField()
    public_key = serializers.CharField(source="publicKey")
    sign_algo = serializers.CharField(source="signAlgo")
    hash_algo = serializers.CharField(source="hashAlgo")
    created_at = serializers.DateTimeField(required=False, allow_null=True, source='createdAt')
    updated_at = serializers.DateTimeField(required=False, allow_null=True, source='updatedAt')


class AccountSerializer(serializers.Serializer):
    address = serializers.CharField(required=True, allow_null=False)
    type = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(required=False, allow_null=True, source='createdAt')
    updated_at = serializers.DateTimeField(required=False, allow_null=True, source='updatedAt')
    deleted_at = serializers.DateTimeField(required=False, allow_null=True, source='deletedAt')


class AccountExtendedSerializer(AccountSerializer):
    keys = KeySerializer(many=True, read_only=True)


class AccountRegisterSerializer(serializers.Serializer):
    job_id = serializers.CharField(required=True, allow_null=False, source="jobId")

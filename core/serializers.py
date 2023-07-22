from rest_framework import serializers


class FirebaseDataSerializer(serializers.Serializer):
    address = serializers.CharField()
    createdAt = serializers.CharField()
    currentFare = serializers.CharField(default="")
    driver_name = serializers.CharField()
    hasMessage = serializers.BooleanField()
    inProgress = serializers.BooleanField()
    messageToken = serializers.CharField(default="")
    nid = serializers.CharField()
    nidPicture = serializers.CharField()
    passenger = serializers.CharField(default="")
    paymentDueDate = serializers.CharField(default="")
    phone = serializers.CharField()
    platformFee = serializers.IntegerField(default=0)
    raters = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)
    totalFare = serializers.IntegerField(default=0)
    totalIncome = serializers.IntegerField(default=0)
    transactionId = serializers.CharField(default="")
    uid = serializers.CharField()
    vehicle = serializers.CharField(required=False)

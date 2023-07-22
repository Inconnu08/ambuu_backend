from django.http import JsonResponse
from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials, messaging, firestore
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from core.serializers import FirebaseDataSerializer

firebase_cred = credentials.Certificate("firebase.json")
firebase_app = firebase_admin.initialize_app(firebase_cred)


def get_tokens_from_firestore(city):
    # Create a Firestore client
    db = firestore.client()

    # Define the Firestore path
    path = f"driver_tokens_{city}"

    # Get all documents in the "city" collection
    docs = db.collection(path).get()

    # Initialize an empty list to store the tokens
    tokens = []

    # Iterate over the documents and extract the tokens
    for doc in docs:
        data = doc.to_dict()
        token = data.get("token")
        if token:
            tokens.append(token)

    return tokens


def subscribe_topic(topic, tokens):
    response = messaging.subscribe_to_topic(tokens, topic)
    if response.failure_count > 0:
        print(f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason, response.errors))}')


def unsubscribe_topic(topic, tokens):  # tokens is a list of registration tokens
    response = messaging.unsubscribe_from_topic(tokens, topic)
    if response.failure_count > 0:
        print(f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason, response.errors))}')


def send_topic_push_notification(title, body, topic, agent):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        topic=topic,
        android=messaging.AndroidConfig(
            priority="high",
            notification=messaging.AndroidNotification(
                sound="default",
                click_action='FLUTTER_NOTIFICATION_CLICK',
                priority='max',
                visibility='public',
                default_vibrate_timings=True,
                channel_id='com.brinotech.ambu_driver.urgent' if agent == 'passenger' else 'com.brinotech.ambu_passenger.urgent',
            )
        ),
        # data={
        #     'click_action': 'FLUTTER_NOTIFICATION_CLICK',
        #     'original_priority': 'high',
        #     'delivered_priority': 'high',
        #     'sound': 'default',
        # }
    )
    messaging.send(message)


def send_token_push_notification(title, body, tokens, agent):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        tokens=tokens,
        android=messaging.AndroidConfig(
            priority="high",
            notification=messaging.AndroidNotification(
                sound="default",
                click_action='FLUTTER_NOTIFICATION_CLICK',
                priority='max',
                visibility='public',
                default_vibrate_timings=True,
                channel_id='com.brinotech.ambu_driver.urgent' if agent == 'passenger' else 'com.brinotech.ambu_passenger.urgent',
            )
        ),
        # data={
        #     'click_action': 'FLUTTER_NOTIFICATION_CLICK',
        #     'google.original_priority': 'high',
        #     'google.delivered_priority': 'high',
        #     'sound': 'default',
        # }
    )
    messaging.send_multicast(message)


def get_driver_tokens(request):
    print(get_tokens_from_firestore("Dhaka"))

    send_topic_push_notification("driver_tokens_Dhaka", "Passenger requested for a ride",
                                 "A passenger nearby is looking for a ride!")
    return JsonResponse({'status': 0}, safe=False, status=status.HTTP_200_OK)


class PostSingleNotificationAPIView(APIView):
    def post(self, request):
        title = request.data.get('title')
        body = request.data.get('body')
        to_token = request.data.get('to')
        agent = request.data.get('agent')

        send_token_push_notification(title, body, [to_token], agent)
        print({'agent': agent, 'message': 'Posted to user successfully', 'title': title, 'body': body, 'to': to_token})

        return Response({'ok': True})


class PostTopicNotificationAPIView(APIView):
    def post(self, request):
        title = request.data.get('title')
        body = request.data.get('body')
        city = request.data.get('city')
        agent = request.data.get('agent')

        send_topic_push_notification(title, body, f"driver_tokens_{city}", agent)
        print({'agent': agent, 'message': 'Posted to topic successfully', 'title': title, 'body': body,
               'to': f"driver_tokens_{city}"})

        return Response({'ok': True})


class FirebaseDataViewSet(ModelViewSet):
    queryset = firestore.client().collection('drivers')
    serializer_class = FirebaseDataSerializer

    def list(self, request, *args, **kwargs):
        response_data = []
        for doc in self.get_queryset().stream():
            data = doc.to_dict()
            response_data.append(data)
        serializer = self.get_serializer(response_data, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        doc_ref = self.get_queryset().document(pk)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            serializer = self.get_serializer(data)
            return Response(serializer.data)
        else:
            return Response({'message': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doc_ref = self.get_queryset().add(serializer.validated_data)
        return Response({'message': 'Data created successfully', 'document_id': doc_ref.id}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        doc_ref = self.get_queryset().document(pk)
        doc = doc_ref.get()
        if doc.exists:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            doc_ref.set(serializer.validated_data)
            return Response({'message': 'Data updated successfully'})
        else:
            return Response({'message': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, *args, **kwargs):
        doc_ref = self.get_queryset().document(pk)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            return Response({'message': 'Data deleted successfully'})
        else:
            return Response({'message': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)

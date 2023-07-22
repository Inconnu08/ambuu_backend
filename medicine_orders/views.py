from firebase_admin import firestore
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response

from .models import MedicineOrder
from .serializers import MedicineOrderSerializer


class MedicineOrderViewSet(viewsets.ModelViewSet):
    queryset = MedicineOrder.objects.all()
    serializer_class = MedicineOrderSerializer

    def handle_exception(self, exc):
        if isinstance(exc, (ValidationError, ParseError)):
            # Handle validation and parse errors
            return Response(data={'errors': exc.detail}, status=400)

        # Call the superclass method for other exceptions
        return super().handle_exception(exc)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        created_object = serializer.instance
        # Get a reference to the Firestore collection and document
        user_ref = firestore.client().collection("users").document(created_object.uid)
        user_ref.update({"hasMedicineDelivery": created_object.pk})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @action(detail=False, methods=['get'])
    def prescription_pending_orders(self, request):
        orders = self.queryset.filter(delivery_status='pending')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def change_delivery_status(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Get the new delivery status from the request data
        new_delivery_status = serializer.validated_data.get('delivery_status')

        # Perform actions when the delivery status is changed to "complete"
        if new_delivery_status == 'complete':
            # Perform your custom actions here
            # For example, send a notification, update related models, etc.
            # Replace the print statement with your desired actions

            print(f"Order with ID {order.id} is marked as complete. Performing additional actions.")

        # Save the updated delivery status
        serializer.save()

        return Response(serializer.data)

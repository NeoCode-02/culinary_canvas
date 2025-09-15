from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.parsers import MultiPartParser
from rest_framework import generics
from .serializers import FileUploadSerializer

class FileUploadView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = FileUploadSerializer
    
    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        responses={201: FileUploadSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
from rest_framework import serializers
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def create(self, validated_data):
        file = validated_data['file']
        return file
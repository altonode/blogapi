from rest_framework import serializers

from postings.models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
	url =  serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = BlogPost
		fields = ['url', 'pk', 'user', 'title', 'content', 'timestamp', ]
		read_only_fields = ['user']
		
	def get_url(self, obj):
		request = self.context.get("request")
		return obj.get_api_url(request=request)